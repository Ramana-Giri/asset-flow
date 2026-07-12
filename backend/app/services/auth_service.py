from __future__ import annotations
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional

from app.repositories.user_repository import UserRepository
from app.db.models.session import UserSession
from app.db.models.password_reset import PasswordResetToken
from app.core.security import hash_password, verify_password, generate_session_token
from app.core.exceptions import NotFoundException, ValidationError, PermissionDenied
from app.services.activity_log_service import ActivityLogService
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession


class AuthService:
    def __init__(
        self,
        session: AsyncSession,
        user_repository: UserRepository,
        activity_log_service: ActivityLogService,
        session_expire_minutes: int = 60 * 24,
    ):
        self.session = session
        self.users = user_repository
        self.activity_log = activity_log_service
        self.session_expire_minutes = session_expire_minutes

    async def signup(self, name: str, email: str, password: str, ip_address: Optional[str] = None):
        existing = await self.users.find_by_email(email)
        if existing is not None:
            raise ValidationError("Email is already registered")
        user = await self.users.create(
            {
                "name": name,
                "email": email,
                "password_hash": hash_password(password),
                "role": "Employee",
            }
        )
        await self.activity_log.log(
            user_id=user.id, action="SIGNUP", entity_type="User", entity_id=user.id, ip_address=ip_address
        )
        return user

    async def login(
        self, email: str, password: str, ip_address: Optional[str] = None, user_agent: Optional[str] = None
    ):
        user = await self.users.find_by_email(email)
        if user is None or not verify_password(password, user.password_hash):
            raise ValidationError("Invalid email or password")
        if user.status != "Active":
            raise PermissionDenied("Account is inactive")

        token = generate_session_token()
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=self.session_expire_minutes)
        user_session = UserSession(
            user_id=user.id,
            session_token=token,
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=expires_at,
        )
        self.session.add(user_session)
        await self.session.flush()

        await self.activity_log.log(
            user_id=user.id, action="LOGIN", entity_type="User", entity_id=user.id, ip_address=ip_address
        )
        return {"session_token": token, "expires_at": expires_at, "user": user}

    async def logout(self, session_token: str):
        result = await self.session.execute(
            select(UserSession).where(UserSession.session_token == session_token)
        )
        user_session = result.scalar_one_or_none()
        if user_session is None:
            return
        user_id = user_session.user_id
        await self.session.delete(user_session)
        await self.session.flush()
        await self.activity_log.log(user_id=user_id, action="LOGOUT", entity_type="User", entity_id=user_id)

    async def validate_session(self, session_token: str):
        result = await self.session.execute(
            select(UserSession).where(UserSession.session_token == session_token)
        )
        user_session = result.scalar_one_or_none()
        if user_session is None:
            return None
        if user_session.expires_at < datetime.now(timezone.utc):
            return None
        user_session.last_active_at = datetime.now(timezone.utc)
        await self.session.flush()
        return await self.users.find_by_id(user_session.user_id)

    async def forgot_password(self, email: str):
        user = await self.users.find_by_email(email)
        if user is None:
            # Do not reveal whether the email exists
            return
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
        reset_token = PasswordResetToken(user_id=user.id, token=token, expires_at=expires_at)
        self.session.add(reset_token)
        await self.session.flush()
        # Sending the actual email/reset link is delegated to a notification/email util (out of scope here).
        await self.activity_log.log(
            user_id=user.id, action="FORGOT_PASSWORD_REQUESTED", entity_type="User", entity_id=user.id
        )
        return reset_token

    async def reset_password(self, token: str, new_password: str):
        result = await self.session.execute(
            select(PasswordResetToken).where(PasswordResetToken.token == token)
        )
        reset_token = result.scalar_one_or_none()
        if reset_token is None or reset_token.used or reset_token.expires_at < datetime.now(timezone.utc):
            raise ValidationError("Invalid or expired reset token")

        user = await self.users.find_by_id(reset_token.user_id)
        if user is None:
            raise NotFoundException("User not found")

        user.password_hash = hash_password(new_password)
        reset_token.used = True

        await self.session.execute(delete(UserSession).where(UserSession.user_id == user.id))
        await self.session.flush()

        await self.activity_log.log(
            user_id=user.id, action="PASSWORD_RESET", entity_type="User", entity_id=user.id
        )
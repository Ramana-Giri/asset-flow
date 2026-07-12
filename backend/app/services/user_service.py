from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional

from app.repositories.user_repository import UserRepository
from app.core.security import hash_password
from app.core.exceptions import NotFoundException, PermissionDenied, ValidationError
from app.services.activity_log_service import ActivityLogService
from app.services.notification_service import NotificationService


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
        activity_log_service: ActivityLogService,
        notification_service: NotificationService,
    ):
        self.users = user_repository
        self.activity_log = activity_log_service
        self.notifications = notification_service

    async def list_users(self, filters: dict, skip: int = 0, limit: int = 50):
        return await self.users.search(filters, skip, limit)

    async def get_user(self, user_id: int):
        user = await self.users.find_by_id(user_id)
        if user is None:
            raise NotFoundException(f"User {user_id} not found")
        return user

    async def create_user(self, name: str, email: str, password: str, department_id: Optional[int], actor_id: int):
        existing = await self.users.find_by_email(email)
        if existing is not None:
            raise ValidationError("Email is already registered")
        user = await self.users.create(
            {
                "name": name,
                "email": email,
                "password_hash": hash_password(password),
                "department_id": department_id,
                "role": "Employee",
            }
        )
        await self.activity_log.log(
            user_id=actor_id, action="CREATE_USER", entity_type="User", entity_id=user.id
        )
        return user

    async def update_user(self, user_id: int, data: dict, actor_id: int):
        user = await self.users.update(user_id, data)
        if user is None:
            raise NotFoundException(f"User {user_id} not found")
        await self.activity_log.log(
            user_id=actor_id, action="UPDATE_USER", entity_type="User", entity_id=user_id, details=data
        )
        return user

    async def set_department(self, user_id: int, department_id: Optional[int], actor_id: int):
        user = await self.users.update(user_id, {"department_id": department_id})
        if user is None:
            raise NotFoundException(f"User {user_id} not found")
        await self.activity_log.log(
            user_id=actor_id,
            action="ASSIGN_DEPARTMENT",
            entity_type="User",
            entity_id=user_id,
            details={"department_id": department_id},
        )
        return user

    async def promote_role(self, user_id: int, new_role: str, actor: dict, actor_id: int):
        if actor.get("role") != "Admin":
            raise PermissionDenied("Only Admin can promote roles")
        if new_role not in ("Department Head", "Asset Manager"):
            raise ValidationError("Role must be 'Department Head' or 'Asset Manager'")

        user = await self.users.update_role(
            user_id, new_role, promoted_by=actor_id, promoted_at=datetime.now(timezone.utc)
        )
        if user is None:
            raise NotFoundException(f"User {user_id} not found")

        await self.notifications.notify(
            user_id=user_id,
            type="Role Promoted",
            title="You've been promoted",
            message=f"You have been promoted to {new_role}.",
            reference_type="User",
            reference_id=user_id,
        )
        await self.activity_log.log(
            user_id=actor_id,
            action="PROMOTE_USER",
            entity_type="User",
            entity_id=user_id,
            details={"new_role": new_role},
        )
        return user

    async def activate_user(self, user_id: int, actor_id: int):
        user = await self.users.set_status(user_id, "Active")
        if user is None:
            raise NotFoundException(f"User {user_id} not found")
        await self.activity_log.log(user_id=actor_id, action="ACTIVATE_USER", entity_type="User", entity_id=user_id)
        return user

    async def deactivate_user(self, user_id: int, actor_id: int):
        user = await self.users.set_status(user_id, "Inactive")
        if user is None:
            raise NotFoundException(f"User {user_id} not found")
        await self.activity_log.log(
            user_id=actor_id, action="DEACTIVATE_USER", entity_type="User", entity_id=user_id
        )
        return user
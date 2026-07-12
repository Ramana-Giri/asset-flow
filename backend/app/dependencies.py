"""
Reusable FastAPI Dependencies

Purpose
-------
Shared Depends() providers for DB sessions, current-user resolution, and role-based authorization gates.

Responsibilities
-----------------
- get_db(): yield a request-scoped AsyncSession.
- get_current_user(): resolve the User from the session token (cookie/header), via AuthService.validate_session().
- get_current_admin() / get_current_asset_manager() / get_current_department_head(): role-guard dependencies.
- These functions ONLY validate authentication and authorization - no business logic.

Interacts With
--------------
- db/database.py -> SessionLocal used by get_db().
- services/auth_service.py -> AuthService.validate_session() used by get_current_user().
- core/permissions.py -> role-checking helpers reused by the role-guard dependencies.
- api/v1/*.py -> every protected route depends on one of these.
"""

from typing import AsyncIterator

from fastapi import Cookie, Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.exceptions import PermissionDenied
from app.core.permissions import (
    require_admin,
    require_asset_manager,
    require_department_head,
)
from app.db.database import SessionLocal
from app.services.auth_service import AuthService


async def get_db() -> AsyncIterator[AsyncSession]:
    """Yield a request-scoped AsyncSession, closing it after the request completes."""
    async with SessionLocal() as session:
        yield session


def _extract_session_token(
    authorization: str | None,
    cookie_token: str | None,
) -> str | None:
    """
    Pull the opaque session token out of either the Authorization header
    (`Bearer <token>`) or the session cookie, preferring the header when
    both are present. This is NOT JWT parsing - the token is an opaque
    random string looked up against `user_sessions.session_token`.
    """
    if authorization:
        scheme, _, value = authorization.partition(" ")
        if scheme.lower() == "bearer" and value:
            return value
    return cookie_token


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    authorization: str | None = Header(default=None),
    session_cookie: str | None = Cookie(default=None, alias=settings.SESSION_COOKIE_NAME),
):
    """
    Resolve the current User from the session token (sent as a Bearer
    header or HttpOnly cookie - NOT a JWT). Raises 401 if missing/invalid/expired.
    """
    token = _extract_session_token(authorization, session_cookie)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated: no session token provided.",
        )

    auth_service = AuthService(db)
    user = await auth_service.validate_session(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session is invalid or has expired.",
        )
    return user


async def get_current_admin(user=Depends(get_current_user)):
    """Raise 403 unless the current user's role == 'Admin'."""
    try:
        require_admin(user)
    except PermissionDenied as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=exc.message) from exc
    return user


async def get_current_asset_manager(user=Depends(get_current_user)):
    """Raise 403 unless the current user's role == 'Asset Manager' (or Admin)."""
    try:
        require_asset_manager(user)
    except PermissionDenied as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=exc.message) from exc
    return user


async def get_current_department_head(user=Depends(get_current_user)):
    """Raise 403 unless the current user's role == 'Department Head' (or Admin)."""
    try:
        require_department_head(user)
    except PermissionDenied as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=exc.message) from exc
    return user
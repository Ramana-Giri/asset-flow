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

NOTE: This file is a structural skeleton only. Method/function bodies are
intentionally left as `pass` (no business logic / SQL / validation code),
per generation scope. Docstrings describe what each piece IS responsible
for once implemented.
"""

from fastapi import Depends, Header


async def get_db():
    """Yield a request-scoped AsyncSession, closing it after the request completes."""
    pass


async def get_current_user(session_token: str | None = Header(default=None)):
    """
    Resolve the current User from the session token (sent as a Bearer
    header or HttpOnly cookie - NOT a JWT). Raises 401 if missing/invalid/expired.
    """
    pass


async def get_current_admin(user=Depends(get_current_user)):
    """Raise 403 unless the current user's role == 'Admin'."""
    pass


async def get_current_asset_manager(user=Depends(get_current_user)):
    """Raise 403 unless the current user's role == 'Asset Manager' (or Admin)."""
    pass


async def get_current_department_head(user=Depends(get_current_user)):
    """Raise 403 unless the current user's role == 'Department Head' (or Admin)."""
    pass

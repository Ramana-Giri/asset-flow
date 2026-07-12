"""
Authorization Helpers

Purpose
-------
Reusable role-validation and permission-checking logic, shared by dependencies.py and services that need defense-in-depth role checks.

Responsibilities
-----------------
- require_admin(user): raise PermissionDenied unless role == 'Admin'.
- require_asset_manager(user): raise PermissionDenied unless role in ('Asset Manager','Admin').
- require_department_head(user): raise PermissionDenied unless role in ('Department Head','Admin').
- require_self_or_admin(user, target_user_id): for endpoints where a user may act on their own record or an Admin may act on anyone's.

Interacts With
--------------
- dependencies.py -> role-guard Depends() providers call these.
- services/*.py -> services may call these again for defense-in-depth beyond the router dependency.
- core/exceptions.py -> raises PermissionDenied on failure.
"""

from app.core.enums import UserRole
from app.core.exceptions import PermissionDenied


def require_admin(user) -> None:
    """Raise PermissionDenied unless the user's role is 'Admin'."""
    if user is None or user.role != UserRole.ADMIN:
        raise PermissionDenied("This action requires Admin privileges.")


def require_asset_manager(user) -> None:
    """Raise PermissionDenied unless the user's role is 'Asset Manager' or 'Admin'."""
    if user is None or user.role not in (UserRole.ASSET_MANAGER, UserRole.ADMIN):
        raise PermissionDenied("This action requires Asset Manager (or Admin) privileges.")


def require_department_head(user) -> None:
    """Raise PermissionDenied unless the user's role is 'Department Head' or 'Admin'."""
    if user is None or user.role not in (UserRole.DEPARTMENT_HEAD, UserRole.ADMIN):
        raise PermissionDenied("This action requires Department Head (or Admin) privileges.")
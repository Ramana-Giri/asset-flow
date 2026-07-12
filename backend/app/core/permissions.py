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

NOTE: This file is a structural skeleton only. Method/function bodies are
intentionally left as `pass` (no business logic / SQL / validation code),
per generation scope. Docstrings describe what each piece IS responsible
for once implemented.
"""
def require_admin(user: "User") -> None:
    if user.role != UserRole.ADMIN:
        raise PermissionDenied("This action requires Admin privileges.")

def require_asset_manager(user: "User") -> None:
    if user.role not in (UserRole.ASSET_MANAGER, UserRole.ADMIN):
        raise PermissionDenied("This action requires Asset Manager (or Admin) privileges.")

def require_department_head(user: "User") -> None:
    if user.role not in (UserRole.DEPARTMENT_HEAD, UserRole.ADMIN):
        raise PermissionDenied("This action requires Department Head (or Admin) privileges.")

def require_self_or_admin(user: "User", target_user_id: int) -> None:
    if user.role != UserRole.ADMIN and user.id != target_user_id:
        raise PermissionDenied("You may only perform this action on your own account.")
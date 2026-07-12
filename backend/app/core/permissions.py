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

def require_admin(user) -> None:
    """Raise PermissionDenied unless the user's role is 'Admin'."""
    pass


def require_asset_manager(user) -> None:
    """Raise PermissionDenied unless the user's role is 'Asset Manager' or 'Admin'."""
    pass


def require_department_head(user) -> None:
    """Raise PermissionDenied unless the user's role is 'Department Head' or 'Admin'."""
    pass


def require_self_or_admin(user, target_user_id: int) -> None:
    """Raise PermissionDenied unless the user is acting on their own record or is Admin."""
    pass

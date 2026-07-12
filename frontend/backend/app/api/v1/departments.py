"""
Departments Router

Purpose
-------
HTTP endpoints for the Departments module, mounted under prefix "/departments".

Responsibilities
-----------------
- Receive the HTTP request and validate it against the Pydantic schema.
- Delegate ALL business logic to DepartmentService - routers never contain business rules or SQL.
- Translate domain exceptions (core/exceptions.py) into HTTP error responses.
- Wrap successful results in the standard {success, message, data} envelope (core/responses.py).

Interacts With
--------------
- schemas/departments.py -> request/response models.
- services/departments_service.py -> DepartmentService, injected via dependencies.py.
- dependencies.py -> get_current_user() / role-guard dependencies applied per-route as needed.

NOTE: This file is a structural skeleton only. Method/function bodies are
intentionally left as `pass` (no business logic / SQL / validation code),
per generation scope. Docstrings describe what each piece IS responsible
for once implemented.
"""

from fastapi import APIRouter, Depends

router = APIRouter(prefix="/departments", tags=["Departments"])

# Role-guard dependencies (from dependencies.py: get_current_user,
# get_current_admin, get_current_asset_manager, get_current_department_head)
# would be added per-route via `Depends(...)` where the requirements
# specify a role restriction (see docstrings below).


@router.get("")
async def list_departments():
    """
    List/search departments (Screen 3, Tab A).

    Flow: receive request -> validate schema -> call DepartmentService.list_departments() -> return standard envelope.
    """
    pass

@router.get("/{department_id}")
async def get_department():
    """
    Fetch a single department, incl. hierarchy.

    Flow: receive request -> validate schema -> call DepartmentService.get_department() -> return standard envelope.
    """
    pass

@router.post("")
async def create_department():
    """
    Admin-only: create a department.

    Flow: receive request -> validate schema -> call DepartmentService.create_department() -> return standard envelope.
    """
    pass

@router.put("/{department_id}")
async def update_department():
    """
    Admin-only: edit a department (blocks circular parent).

    Flow: receive request -> validate schema -> call DepartmentService.update_department() -> return standard envelope.
    """
    pass

@router.patch("/{department_id}/head")
async def assign_head():
    """
    Admin-only: assign the Department Head.

    Flow: receive request -> validate schema -> call DepartmentService.assign_head() -> return standard envelope.
    """
    pass

@router.patch("/{department_id}/deactivate")
async def deactivate_department():
    """
    Admin-only: deactivate a department.

    Flow: receive request -> validate schema -> call DepartmentService.deactivate_department() -> return standard envelope.
    """
    pass

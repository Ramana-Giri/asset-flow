"""
Dashboard Router

Purpose
-------
HTTP endpoints for the Dashboard module, mounted under prefix "/dashboard".

Responsibilities
-----------------
- Receive the HTTP request and validate it against the Pydantic schema.
- Delegate ALL business logic to DashboardService - routers never contain business rules or SQL.
- Translate domain exceptions (core/exceptions.py) into HTTP error responses.
- Wrap successful results in the standard {success, message, data} envelope (core/responses.py).

Interacts With
--------------
- schemas/dashboard.py -> request/response models.
- services/dashboard_service.py -> DashboardService, injected via dependencies.py.
- dependencies.py -> get_current_user() / role-guard dependencies applied per-route as needed.

NOTE: This file is a structural skeleton only. Method/function bodies are
intentionally left as `pass` (no business logic / SQL / validation code),
per generation scope. Docstrings describe what each piece IS responsible
for once implemented.
"""

from fastapi import APIRouter, Depends

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

# Role-guard dependencies (from dependencies.py: get_current_user,
# get_current_admin, get_current_asset_manager, get_current_department_head)
# would be added per-route via `Depends(...)` where the requirements
# specify a role restriction (see docstrings below).


@router.get("/kpis")
async def get_kpis():
    """
    KPI cards for the Dashboard screen (Screen 2).

    Flow: receive request -> validate schema -> call DashboardService.get_kpis() -> return standard envelope.
    """
    pass

@router.get("/recent-activity")
async def get_recent_activity():
    """
    Recent activity feed for the dashboard.

    Flow: receive request -> validate schema -> call DashboardService.get_recent_activity() -> return standard envelope.
    """
    pass

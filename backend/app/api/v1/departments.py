from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user, get_current_admin
from app.core.responses import success
from app.repositories.department_repository import DepartmentRepository
from app.repositories.user_repository import UserRepository
from app.repositories.activity_log_repository import ActivityLogRepository
from app.repositories.notification_repository import NotificationRepository
from app.services.department_service import DepartmentService
from app.services.activity_log_service import ActivityLogService
from app.services.notification_service import NotificationService
from app.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentFilter

router = APIRouter(prefix="/departments", tags=["Departments"])


def get_department_service(db: AsyncSession = Depends(get_db)) -> DepartmentService:
    return DepartmentService(
        DepartmentRepository(db),
        UserRepository(db),
        ActivityLogService(ActivityLogRepository(db)),
        NotificationService(NotificationRepository(db)),
    )


@router.get("")
async def list_departments(
    filters: DepartmentFilter = Depends(), skip: int = 0, limit: int = 50, service: DepartmentService = Depends(get_department_service)
):
    page = await service.list_departments(filters.model_dump(exclude_none=True), skip, limit)
    return success(data={"items": page.items, "total": page.total, "skip": page.skip, "limit": page.limit})


@router.get("/{department_id}")
async def get_department(department_id: int, service: DepartmentService = Depends(get_department_service)):
    department = await service.get_department(department_id)
    return success(data=department)


@router.post("")
async def create_department(
    payload: DepartmentCreate, service: DepartmentService = Depends(get_department_service), admin=Depends(get_current_admin)
):
    department = await service.create_department(
        payload.name, payload.parent_department_id, payload.head_user_id, admin.id
    )
    return success(data=department, message="Department created")


@router.put("/{department_id}")
async def update_department(
    department_id: int,
    payload: DepartmentUpdate,
    service: DepartmentService = Depends(get_department_service),
    admin=Depends(get_current_admin),
):
    department = await service.update_department(department_id, payload.model_dump(exclude_none=True), admin.id)
    return success(data=department, message="Department updated")


@router.patch("/{department_id}/head")
async def assign_head(
    department_id: int, head_user_id: int, service: DepartmentService = Depends(get_department_service), admin=Depends(get_current_admin)
):
    department = await service.assign_head(department_id, head_user_id, admin.id)
    return success(data=department, message="Department Head assigned")


@router.patch("/{department_id}/deactivate")
async def deactivate_department(
    department_id: int, service: DepartmentService = Depends(get_department_service), admin=Depends(get_current_admin)
):
    department = await service.deactivate_department(department_id, admin.id)
    return success(data=department, message="Department deactivated")
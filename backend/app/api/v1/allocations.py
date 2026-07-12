from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_asset_manager
from app.core.responses import success
from app.repositories.allocation_repository import AllocationRepository
from app.repositories.asset_repository import AssetRepository
from app.repositories.asset_category_repository import AssetCategoryRepository
from app.repositories.department_repository import DepartmentRepository
from app.repositories.maintenance_repository import MaintenanceRepository
from app.repositories.activity_log_repository import ActivityLogRepository
from app.repositories.notification_repository import NotificationRepository
from app.services.allocation_service import AllocationService
from app.services.asset_service import AssetService
from app.services.notification_service import NotificationService
from app.services.activity_log_service import ActivityLogService
from app.schemas.allocation import AllocationCreate, AllocationReturn

router = APIRouter(prefix="/allocations", tags=["Allocations"])


def get_allocation_service(db: AsyncSession = Depends(get_db)) -> AllocationService:
    asset_service = AssetService(
        AssetRepository(db),
        AssetCategoryRepository(db),
        DepartmentRepository(db),
        AllocationRepository(db),
        MaintenanceRepository(db),
        ActivityLogService(ActivityLogRepository(db)),
    )
    return AllocationService(
        AllocationRepository(db),
        AssetRepository(db),
        asset_service,
        NotificationService(NotificationRepository(db)),
        ActivityLogService(ActivityLogRepository(db)),
    )


@router.post("")
async def allocate_asset(
    payload: AllocationCreate, service: AllocationService = Depends(get_allocation_service), actor=Depends(get_current_asset_manager)
):
    allocation = await service.allocate_asset(
        asset_id=payload.asset_id,
        allocated_to_type=payload.allocated_to_type,
        allocated_by=actor.id,
        allocated_to_user_id=payload.allocated_to_user_id,
        allocated_to_department_id=payload.allocated_to_department_id,
        expected_return_date=payload.expected_return_date,
    )
    return success(data=allocation, message="Asset allocated")


@router.post("/{asset_id}/return")
async def return_asset(
    asset_id: int, payload: AllocationReturn, service: AllocationService = Depends(get_allocation_service), actor=Depends(get_current_asset_manager)
):
    allocation = await service.return_asset(asset_id, actor.id, payload.return_condition_notes)
    return success(data=allocation, message="Asset returned")


@router.get("/overdue")
async def list_overdue(service: AllocationService = Depends(get_allocation_service)):
    overdue = await service.list_overdue_allocations()
    return success(data=overdue)


@router.get("")
async def get_allocation_history(
    user_id: int | None = None, department_id: int | None = None, service: AllocationService = Depends(get_allocation_service)
):
    history = await service.get_allocation_history(user_id=user_id, department_id=department_id)
    return success(data=history)
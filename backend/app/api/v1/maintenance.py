from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user, get_current_asset_manager
from app.core.responses import success
from app.repositories.maintenance_repository import MaintenanceRepository
from app.repositories.asset_repository import AssetRepository
from app.repositories.asset_category_repository import AssetCategoryRepository
from app.repositories.department_repository import DepartmentRepository
from app.repositories.allocation_repository import AllocationRepository
from app.repositories.activity_log_repository import ActivityLogRepository
from app.repositories.notification_repository import NotificationRepository
from app.services.maintenance_service import MaintenanceService
from app.services.asset_service import AssetService
from app.services.notification_service import NotificationService
from app.services.activity_log_service import ActivityLogService
from app.schemas.maintenance import (
    MaintenanceRequestCreate, MaintenanceDecision, MaintenanceTechnicianAssign, MaintenanceResolve,
)

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])


def get_maintenance_service(db: AsyncSession = Depends(get_db)) -> MaintenanceService:
    asset_service = AssetService(
        AssetRepository(db),
        AssetCategoryRepository(db),
        DepartmentRepository(db),
        AllocationRepository(db),
        MaintenanceRepository(db),
        ActivityLogService(ActivityLogRepository(db)),
    )
    return MaintenanceService(
        MaintenanceRepository(db),
        AssetRepository(db),
        asset_service,
        NotificationService(NotificationRepository(db)),
        ActivityLogService(ActivityLogRepository(db)),
    )


@router.post("")
async def raise_request(
    payload: MaintenanceRequestCreate, service: MaintenanceService = Depends(get_maintenance_service), actor=Depends(get_current_user)
):
    request = await service.raise_request(
        payload.asset_id, actor.id, payload.issue_description, payload.priority, payload.photo_url
    )
    return success(data=request, message="Maintenance request raised")


@router.patch("/{request_id}/decision")
async def decide_request(
    request_id: int,
    payload: MaintenanceDecision,
    service: MaintenanceService = Depends(get_maintenance_service),
    actor=Depends(get_current_asset_manager),
):
    if payload.approve:
        request = await service.approve_request(request_id, actor.id, actor.role)
        return success(data=request, message="Maintenance request approved")
    request = await service.reject_request(request_id, actor.id, payload.rejection_reason)
    return success(data=request, message="Maintenance request rejected")


@router.patch("/{request_id}/technician")
async def assign_technician(
    request_id: int,
    payload: MaintenanceTechnicianAssign,
    service: MaintenanceService = Depends(get_maintenance_service),
    actor=Depends(get_current_asset_manager),
):
    request = await service.assign_technician(request_id, payload.technician_name, payload.technician_contact, actor.id)
    return success(data=request, message="Technician assigned")


@router.patch("/{request_id}/start")
async def start_progress(
    request_id: int, service: MaintenanceService = Depends(get_maintenance_service), actor=Depends(get_current_asset_manager)
):
    request = await service.start_progress(request_id, actor.id)
    return success(data=request, message="Maintenance in progress")


@router.patch("/{request_id}/resolve")
async def resolve_request(
    request_id: int,
    payload: MaintenanceResolve,
    service: MaintenanceService = Depends(get_maintenance_service),
    actor=Depends(get_current_asset_manager),
):
    request = await service.resolve_request(request_id, payload.resolution_notes, actor.id)
    return success(data=request, message="Maintenance resolved")


@router.get("/asset/{asset_id}")
async def get_maintenance_history(asset_id: int, service: MaintenanceService = Depends(get_maintenance_service)):
    history = await service.get_maintenance_history(asset_id)
    return success(data=history)
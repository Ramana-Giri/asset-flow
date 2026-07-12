from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user, get_current_asset_manager
from app.core.responses import success
from app.repositories.transfer_repository import TransferRepository
from app.repositories.allocation_repository import AllocationRepository
from app.repositories.asset_repository import AssetRepository
from app.repositories.asset_category_repository import AssetCategoryRepository
from app.repositories.department_repository import DepartmentRepository
from app.repositories.maintenance_repository import MaintenanceRepository
from app.repositories.activity_log_repository import ActivityLogRepository
from app.repositories.notification_repository import NotificationRepository
from app.services.transfer_service import TransferService
from app.services.allocation_service import AllocationService
from app.services.asset_service import AssetService
from app.services.notification_service import NotificationService
from app.services.activity_log_service import ActivityLogService
from app.schemas.transfer import TransferRequestCreate, TransferDecision

router = APIRouter(prefix="/transfers", tags=["Transfers"])


def get_transfer_service(db: AsyncSession = Depends(get_db)) -> TransferService:
    asset_service = AssetService(
        AssetRepository(db),
        AssetCategoryRepository(db),
        DepartmentRepository(db),
        AllocationRepository(db),
        MaintenanceRepository(db),
        ActivityLogService(ActivityLogRepository(db)),
    )
    allocation_service = AllocationService(
        AllocationRepository(db),
        AssetRepository(db),
        asset_service,
        NotificationService(NotificationRepository(db)),
        ActivityLogService(ActivityLogRepository(db)),
    )
    return TransferService(
        TransferRepository(db),
        AllocationRepository(db),
        AssetRepository(db),
        allocation_service,
        NotificationService(NotificationRepository(db)),
        ActivityLogService(ActivityLogRepository(db)),
    )


@router.post("")
async def request_transfer(
    payload: TransferRequestCreate, service: TransferService = Depends(get_transfer_service), actor=Depends(get_current_user)
):
    transfer = await service.request_transfer(
        payload.asset_id, actor.id, payload.to_user_id, payload.to_department_id, payload.reason
    )
    return success(data=transfer, message="Transfer requested")


@router.patch("/{transfer_id}/decision")
async def decide_transfer(
    transfer_id: int,
    payload: TransferDecision,
    service: TransferService = Depends(get_transfer_service),
    actor=Depends(get_current_asset_manager),
):
    if payload.approve:
        transfer = await service.approve_transfer(transfer_id, actor.id, actor.role)
        return success(data=transfer, message="Transfer approved")
    transfer = await service.reject_transfer(transfer_id, actor.id)
    return success(data=transfer, message="Transfer rejected")


@router.get("/asset/{asset_id}")
async def get_transfer_history(asset_id: int, service: TransferService = Depends(get_transfer_service)):
    history = await service.get_transfer_history(asset_id)
    return success(data=history)
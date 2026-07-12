from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user
from app.core.responses import success
from app.repositories.asset_repository import AssetRepository
from app.repositories.allocation_repository import AllocationRepository
from app.repositories.maintenance_repository import MaintenanceRepository
from app.repositories.booking_repository import BookingRepository
from app.repositories.transfer_repository import TransferRepository
from app.repositories.activity_log_repository import ActivityLogRepository
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


def get_dashboard_service(db: AsyncSession = Depends(get_db)) -> DashboardService:
    return DashboardService(
        AssetRepository(db),
        AllocationRepository(db),
        MaintenanceRepository(db),
        BookingRepository(db),
        TransferRepository(db),
        ActivityLogRepository(db),
    )


@router.get("/kpis")
async def get_kpis(service: DashboardService = Depends(get_dashboard_service), actor=Depends(get_current_user)):
    kpis = await service.get_kpis()
    return success(data=kpis)


@router.get("/recent-activity")
async def get_recent_activity(
    limit: int = 20, service: DashboardService = Depends(get_dashboard_service), actor=Depends(get_current_user)
):
    activity = await service.get_recent_activity(limit)
    return success(data=activity)
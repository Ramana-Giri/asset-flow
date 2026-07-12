from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_asset_manager
from app.core.responses import success
from app.repositories.report_repository import ReportRepository
from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["Reports"])


def get_report_service(db: AsyncSession = Depends(get_db)) -> ReportService:
    return ReportService(ReportRepository(db))


@router.get("/asset-utilization")
async def asset_utilization(service: ReportService = Depends(get_report_service), actor=Depends(get_current_asset_manager)):
    data = await service.asset_utilization()
    return success(data={"items": data})


@router.get("/department-summary")
async def department_summary(service: ReportService = Depends(get_report_service), actor=Depends(get_current_asset_manager)):
    data = await service.department_summary()
    return success(data={"items": data})


@router.get("/maintenance-summary")
async def maintenance_summary(service: ReportService = Depends(get_report_service), actor=Depends(get_current_asset_manager)):
    data = await service.maintenance_summary()
    return success(data={"items": data})


@router.get("/booking-heatmap")
async def booking_heatmap(service: ReportService = Depends(get_report_service), actor=Depends(get_current_asset_manager)):
    data = await service.booking_heatmap()
    return success(data={"items": data})


@router.get("/idle-assets")
async def idle_assets(
    days: int = 90, service: ReportService = Depends(get_report_service), actor=Depends(get_current_asset_manager)
):
    data = await service.idle_assets(days)
    return success(data={"items": data, "threshold_days": days})
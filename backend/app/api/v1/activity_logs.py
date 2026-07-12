from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_admin
from app.core.responses import success
from app.repositories.activity_log_repository import ActivityLogRepository
from app.services.activity_log_service import ActivityLogService
from app.schemas.activity_log import ActivityLogFilter

router = APIRouter(prefix="/activity-logs", tags=["Activity Logs"])


def get_activity_log_service(db: AsyncSession = Depends(get_db)) -> ActivityLogService:
    return ActivityLogService(ActivityLogRepository(db))


@router.get("")
async def search_activity_logs(
    filters: ActivityLogFilter = Depends(),
    skip: int = 0,
    limit: int = 50,
    service: ActivityLogService = Depends(get_activity_log_service),
    admin=Depends(get_current_admin),
):
    page = await service.search(**filters.model_dump(exclude_none=True), skip=skip, limit=limit)
    return success(data={"items": page.items, "total": page.total, "skip": page.skip, "limit": page.limit})
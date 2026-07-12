from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user
from app.core.responses import success
from app.repositories.notification_repository import NotificationRepository
from app.services.notification_service import NotificationService
from app.schemas.notification import NotificationMarkReadRequest

router = APIRouter(prefix="/notifications", tags=["Notifications"])


def get_notification_service(db: AsyncSession = Depends(get_db)) -> NotificationService:
    return NotificationService(NotificationRepository(db))


@router.get("")
async def list_notifications(
    skip: int = 0, limit: int = 50, service: NotificationService = Depends(get_notification_service), actor=Depends(get_current_user)
):
    result = await service.list_for_user(actor.id, skip, limit)
    return success(data=result)


@router.patch("/read")
async def mark_read(
    payload: NotificationMarkReadRequest, service: NotificationService = Depends(get_notification_service), actor=Depends(get_current_user)
):
    count = await service.mark_read(payload.notification_ids)
    return success(data={"updated": count}, message="Notifications marked as read")
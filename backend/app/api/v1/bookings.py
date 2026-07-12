from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user
from app.core.responses import success
from app.repositories.booking_repository import BookingRepository
from app.repositories.asset_repository import AssetRepository
from app.repositories.activity_log_repository import ActivityLogRepository
from app.repositories.notification_repository import NotificationRepository
from app.services.booking_service import BookingService
from app.services.notification_service import NotificationService
from app.services.activity_log_service import ActivityLogService
from app.schemas.booking import BookingCreate, BookingReschedule, BookingCalendarFilter

router = APIRouter(prefix="/bookings", tags=["Bookings"])


def get_booking_service(db: AsyncSession = Depends(get_db)) -> BookingService:
    return BookingService(
        BookingRepository(db),
        AssetRepository(db),
        NotificationService(NotificationRepository(db)),
        ActivityLogService(ActivityLogRepository(db)),
    )


@router.post("")
async def create_booking(
    payload: BookingCreate, service: BookingService = Depends(get_booking_service), actor=Depends(get_current_user)
):
    booking = await service.create_booking(
        payload.asset_id, actor.id, payload.start_time, payload.end_time, payload.purpose, payload.department_id
    )
    return success(data=booking, message="Booking created")


@router.patch("/{booking_id}/cancel")
async def cancel_booking(
    booking_id: int, service: BookingService = Depends(get_booking_service), actor=Depends(get_current_user)
):
    booking = await service.cancel_booking(booking_id, actor.id)
    return success(data=booking, message="Booking cancelled")


@router.patch("/{booking_id}/reschedule")
async def reschedule_booking(
    booking_id: int, payload: BookingReschedule, service: BookingService = Depends(get_booking_service), actor=Depends(get_current_user)
):
    booking = await service.reschedule_booking(booking_id, payload.start_time, payload.end_time, actor.id)
    return success(data=booking, message="Booking rescheduled")


@router.get("/calendar")
async def get_calendar(filters: BookingCalendarFilter = Depends(), service: BookingService = Depends(get_booking_service)):
    bookings = await service.get_calendar(filters.asset_id, filters.range_start, filters.range_end)
    return success(data=bookings)
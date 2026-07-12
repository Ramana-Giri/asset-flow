from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional

from app.repositories.booking_repository import BookingRepository
from app.repositories.asset_repository import AssetRepository
from app.services.notification_service import NotificationService
from app.services.activity_log_service import ActivityLogService
from app.core.exceptions import NotFoundException, ValidationError, BookingOverlapException


class BookingService:
    def __init__(
        self,
        booking_repository: BookingRepository,
        asset_repository: AssetRepository,
        notification_service: NotificationService,
        activity_log_service: ActivityLogService,
    ):
        self.bookings = booking_repository
        self.assets = asset_repository
        self.notifications = notification_service
        self.activity_log = activity_log_service

    async def create_booking(
        self,
        asset_id: int,
        booked_by: int,
        start_time: datetime,
        end_time: datetime,
        purpose: Optional[str] = None,
        department_id: Optional[int] = None,
    ):
        asset = await self.assets.find_by_id(asset_id)
        if asset is None:
            raise NotFoundException(f"Asset {asset_id} not found")
        if not asset.is_bookable:
            raise ValidationError(f"Asset {asset_id} is not bookable")
        if end_time <= start_time:
            raise ValidationError("end_time must be after start_time")

        overlapping = await self.bookings.find_overlapping(asset_id, start_time, end_time)
        if overlapping:
            raise BookingOverlapException(f"Asset {asset_id} already has an overlapping booking")

        booking = await self.bookings.create(
            {
                "asset_id": asset_id,
                "booked_by": booked_by,
                "department_id": department_id,
                "start_time": start_time,
                "end_time": end_time,
                "purpose": purpose,
                "status": "Upcoming",
            }
        )

        await self.notifications.notify(
            user_id=booked_by,
            type="Booking Confirmed",
            title="Booking Confirmed",
            message=f"Your booking for asset #{asset_id} is confirmed.",
            reference_type="Booking",
            reference_id=booking.id,
        )
        await self.activity_log.log(
            user_id=booked_by, action="CREATE_BOOKING", entity_type="Booking", entity_id=booking.id
        )
        return booking

    async def cancel_booking(self, booking_id: int, cancelled_by: int):
        booking = await self.bookings.find_by_id(booking_id)
        if booking is None:
            raise NotFoundException(f"Booking {booking_id} not found")
        if booking.status in ("Completed", "Cancelled"):
            raise ValidationError(f"Booking {booking_id} cannot be cancelled from status '{booking.status}'")

        updated = await self.bookings.cancel(booking_id, cancelled_by, datetime.now(timezone.utc))
        await self.notifications.notify(
            user_id=booking.booked_by,
            type="Booking Cancelled",
            title="Booking Cancelled",
            message=f"Booking #{booking_id} has been cancelled.",
            reference_type="Booking",
            reference_id=booking_id,
        )
        await self.activity_log.log(
            user_id=cancelled_by, action="CANCEL_BOOKING", entity_type="Booking", entity_id=booking_id
        )
        return updated

    async def reschedule_booking(self, booking_id: int, new_start_time: datetime, new_end_time: datetime, actor_id: int):
        booking = await self.bookings.find_by_id(booking_id)
        if booking is None:
            raise NotFoundException(f"Booking {booking_id} not found")
        if new_end_time <= new_start_time:
            raise ValidationError("end_time must be after start_time")

        overlapping = await self.bookings.find_overlapping(
            booking.asset_id, new_start_time, new_end_time, exclude_booking_id=booking_id
        )
        if overlapping:
            raise BookingOverlapException(f"Asset {booking.asset_id} already has an overlapping booking")

        updated = await self.bookings.update(booking_id, {"start_time": new_start_time, "end_time": new_end_time})
        await self.notifications.notify(
            user_id=booking.booked_by,
            type="Booking Confirmed",
            title="Booking Rescheduled",
            message=f"Booking #{booking_id} has been rescheduled.",
            reference_type="Booking",
            reference_id=booking_id,
        )
        await self.activity_log.log(
            user_id=actor_id, action="RESCHEDULE_BOOKING", entity_type="Booking", entity_id=booking_id
        )
        return updated

    async def get_calendar(self, asset_id: int, range_start: datetime, range_end: datetime):
        return await self.bookings.list_by_asset_calendar(asset_id, range_start, range_end)

    async def send_upcoming_reminders(self):
        upcoming = await self.bookings.list_upcoming_for_reminders()
        for booking in upcoming:
            await self.notifications.notify(
                user_id=booking.booked_by,
                type="Booking Reminder",
                title="Upcoming Booking",
                message=f"Your booking for asset #{booking.asset_id} starts at {booking.start_time}.",
                reference_type="Booking",
                reference_id=booking.id,
            )

    async def mark_ongoing_and_completed(self):
        now = datetime.now(timezone.utc)
        upcoming = await self.bookings.list_upcoming_for_reminders()
        for booking in upcoming:
            if booking.start_time <= now < booking.end_time:
                await self.bookings.update(booking.id, {"status": "Ongoing"})
            elif booking.end_time <= now:
                await self.bookings.update(booking.id, {"status": "Completed"})
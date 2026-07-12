from __future__ import annotations
from datetime import datetime
from typing import Optional, Sequence

from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository
from app.db.models.booking import ResourceBooking


class BookingRepository(BaseRepository[ResourceBooking]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ResourceBooking)

    async def find_overlapping(
        self, asset_id: int, start_time: datetime, end_time: datetime, exclude_booking_id: Optional[int] = None
    ) -> Sequence[ResourceBooking]:
        query = select(ResourceBooking).where(
            ResourceBooking.asset_id == asset_id,
            ResourceBooking.status.in_(["Upcoming", "Ongoing"]),
            ResourceBooking.start_time < end_time,
            ResourceBooking.end_time > start_time,
        )
        if exclude_booking_id is not None:
            query = query.where(ResourceBooking.id != exclude_booking_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def list_by_asset_calendar(
        self, asset_id: int, range_start: datetime, range_end: datetime
    ) -> Sequence[ResourceBooking]:
        result = await self.session.execute(
            select(ResourceBooking).where(
                ResourceBooking.asset_id == asset_id,
                ResourceBooking.start_time < range_end,
                ResourceBooking.end_time > range_start,
            )
        )
        return result.scalars().all()

    async def list_upcoming_for_reminders(self) -> Sequence[ResourceBooking]:
        result = await self.session.execute(
            select(ResourceBooking).where(
                ResourceBooking.status == "Upcoming",
                ResourceBooking.start_time > datetime.now(),
            )
        )
        return result.scalars().all()

    async def cancel(
        self, booking_id: int, cancelled_by: int, cancelled_at: datetime
    ) -> Optional[ResourceBooking]:
        booking = await self.find_by_id(booking_id)
        if booking is None:
            return None
        booking.status = "Cancelled"
        booking.cancelled_by = cancelled_by
        booking.cancelled_at = cancelled_at
        await self.session.flush()
        await self.session.refresh(booking)
        return booking
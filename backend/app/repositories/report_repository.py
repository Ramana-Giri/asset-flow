from __future__ import annotations
from datetime import datetime, timedelta
from typing import Optional, Sequence

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.asset import Asset
from app.db.models.allocation import Allocation
from app.db.models.booking import ResourceBooking
from app.db.models.maintenance import MaintenanceRequest


class ReportRepository:
    """Aggregate/analytics queries spanning multiple tables; not tied to a single model."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def asset_utilization(self) -> Sequence[dict]:
        alloc_counts = await self.session.execute(
            select(Allocation.asset_id, func.count().label("allocation_count"))
            .group_by(Allocation.asset_id)
        )
        booking_counts = await self.session.execute(
            select(ResourceBooking.asset_id, func.count().label("booking_count"))
            .group_by(ResourceBooking.asset_id)
        )
        alloc_map = {row.asset_id: row.allocation_count for row in alloc_counts}
        booking_map = {row.asset_id: row.booking_count for row in booking_counts}
        asset_ids = set(alloc_map) | set(booking_map)
        return [
            {
                "asset_id": asset_id,
                "allocation_count": alloc_map.get(asset_id, 0),
                "booking_count": booking_map.get(asset_id, 0),
            }
            for asset_id in asset_ids
        ]

    async def department_summary(self) -> Sequence[dict]:
        result = await self.session.execute(
            select(Allocation.allocated_to_department_id, func.count().label("allocation_count"))
            .where(Allocation.allocated_to_department_id.is_not(None))
            .group_by(Allocation.allocated_to_department_id)
        )
        return [
            {"department_id": row.allocated_to_department_id, "allocation_count": row.allocation_count}
            for row in result
        ]

    async def maintenance_summary(self) -> Sequence[dict]:
        result = await self.session.execute(
            select(MaintenanceRequest.asset_id, func.count().label("request_count"))
            .group_by(MaintenanceRequest.asset_id)
        )
        return [{"asset_id": row.asset_id, "request_count": row.request_count} for row in result]

    async def booking_heatmap(self) -> Sequence[dict]:
        result = await self.session.execute(
            select(
                func.extract("dow", ResourceBooking.start_time).label("weekday"),
                func.extract("hour", ResourceBooking.start_time).label("hour"),
                func.count().label("booking_count"),
            ).group_by("weekday", "hour")
        )
        return [
            {"weekday": int(row.weekday), "hour": int(row.hour), "booking_count": row.booking_count}
            for row in result
        ]

    async def idle_assets(self, days: int = 90) -> Sequence[Asset]:
        cutoff = datetime.now() - timedelta(days=days)
        active_asset_ids_alloc = await self.session.execute(
            select(Allocation.asset_id).where(Allocation.created_at >= cutoff)
        )
        active_asset_ids_booking = await self.session.execute(
            select(ResourceBooking.asset_id).where(ResourceBooking.created_at >= cutoff)
        )
        active_ids = {r for (r,) in active_asset_ids_alloc} | {r for (r,) in active_asset_ids_booking}
        query = select(Asset)
        if active_ids:
            query = query.where(Asset.id.not_in(active_ids))
        result = await self.session.execute(query)
        return result.scalars().all()
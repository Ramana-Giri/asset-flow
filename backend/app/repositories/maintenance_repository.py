from __future__ import annotations
from datetime import date
from typing import Sequence

from sqlalchemy import select, func, cast, Date
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository
from app.db.models.maintenance import MaintenanceRequest


class MaintenanceRepository(BaseRepository[MaintenanceRequest]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, MaintenanceRequest)

    async def list_by_asset(self, asset_id: int) -> Sequence[MaintenanceRequest]:
        result = await self.session.execute(
            select(MaintenanceRequest)
            .where(MaintenanceRequest.asset_id == asset_id)
            .order_by(MaintenanceRequest.created_at.desc())
        )
        return result.scalars().all()

    async def list_by_status(self, status: str) -> Sequence[MaintenanceRequest]:
        result = await self.session.execute(
            select(MaintenanceRequest).where(MaintenanceRequest.status == status)
        )
        return result.scalars().all()

    async def list_due_today(self) -> Sequence[MaintenanceRequest]:
        today = date.today()
        result = await self.session.execute(
            select(MaintenanceRequest).where(
                cast(MaintenanceRequest.technician_assigned_at, Date) == today,
                MaintenanceRequest.status.in_(
                    ["Approved", "Technician Assigned", "In Progress"]
                ),
            )
        )
        assigned_today = result.scalars().all()

        result2 = await self.session.execute(
            select(MaintenanceRequest).where(
                cast(MaintenanceRequest.in_progress_at, Date) == today,
                MaintenanceRequest.status.in_(
                    ["Approved", "Technician Assigned", "In Progress"]
                ),
            )
        )
        in_progress_today = result2.scalars().all()

        seen_ids = set()
        combined = []
        for item in list(assigned_today) + list(in_progress_today):
            if item.id not in seen_ids:
                seen_ids.add(item.id)
                combined.append(item)
        return combined
from __future__ import annotations
from datetime import date, datetime
from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository
from app.db.models.allocation import Allocation


class AllocationRepository(BaseRepository[Allocation]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Allocation)

    async def find_active_by_asset(self, asset_id: int) -> Optional[Allocation]:
        result = await self.session.execute(
            select(Allocation).where(Allocation.asset_id == asset_id, Allocation.status == "Active")
        )
        return result.scalar_one_or_none()

    async def list_by_user(self, user_id: int) -> Sequence[Allocation]:
        result = await self.session.execute(
            select(Allocation).where(Allocation.allocated_to_user_id == user_id)
        )
        return result.scalars().all()

    async def list_by_department(self, department_id: int) -> Sequence[Allocation]:
        result = await self.session.execute(
            select(Allocation).where(Allocation.allocated_to_department_id == department_id)
        )
        return result.scalars().all()

    async def list_overdue(self) -> Sequence[Allocation]:
        result = await self.session.execute(
            select(Allocation).where(
                Allocation.status == "Active",
                Allocation.expected_return_date.is_not(None),
                Allocation.expected_return_date < date.today(),
            )
        )
        return result.scalars().all()

    async def mark_returned(
        self, allocation_id: int, actual_return_date: date, return_condition_notes: Optional[str], returned_by: int
    ) -> Optional[Allocation]:
        allocation = await self.find_by_id(allocation_id)
        if allocation is None:
            return None
        allocation.actual_return_date = actual_return_date
        allocation.return_condition_notes = return_condition_notes
        allocation.returned_by = returned_by
        allocation.status = "Returned"
        await self.session.flush()
        await self.session.refresh(allocation)
        return allocation
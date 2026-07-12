from __future__ import annotations
from datetime import datetime
from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository
from app.db.models.audit_cycle import AuditCycle
from app.db.models.audit_cycle_auditor import AuditCycleAuditor
from app.db.models.audit_item import AuditItem


class AuditRepository(BaseRepository[AuditCycle]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, AuditCycle)

    async def assign_auditors(self, audit_cycle_id: int, auditor_ids: list[int]) -> Sequence[AuditCycleAuditor]:
        rows = [
            AuditCycleAuditor(audit_cycle_id=audit_cycle_id, auditor_id=auditor_id)
            for auditor_id in auditor_ids
        ]
        self.session.add_all(rows)
        await self.session.flush()
        for row in rows:
            await self.session.refresh(row)
        return rows

    async def list_items_by_cycle(self, audit_cycle_id: int) -> Sequence[AuditItem]:
        result = await self.session.execute(
            select(AuditItem).where(AuditItem.audit_cycle_id == audit_cycle_id)
        )
        return result.scalars().all()

    async def upsert_item_result(
        self, audit_cycle_id: int, asset_id: int, auditor_id: int, result: str, remarks: Optional[str], checked_at: datetime
    ) -> AuditItem:
        existing = await self.session.execute(
            select(AuditItem).where(
                AuditItem.audit_cycle_id == audit_cycle_id, AuditItem.asset_id == asset_id
            )
        )
        item = existing.scalar_one_or_none()
        if item is None:
            item = AuditItem(
                audit_cycle_id=audit_cycle_id,
                asset_id=asset_id,
                auditor_id=auditor_id,
                result=result,
                remarks=remarks,
                checked_at=checked_at,
            )
            self.session.add(item)
        else:
            item.auditor_id = auditor_id
            item.result = result
            item.remarks = remarks
            item.checked_at = checked_at
        await self.session.flush()
        await self.session.refresh(item)
        return item

    async def list_discrepancies(self, audit_cycle_id: int) -> Sequence[AuditItem]:
        result = await self.session.execute(
            select(AuditItem).where(
                AuditItem.audit_cycle_id == audit_cycle_id,
                AuditItem.result.in_(["Missing", "Damaged"]),
            )
        )
        return result.scalars().all()

    async def close_cycle(self, audit_cycle_id: int, closed_by: int, closed_at: datetime) -> Optional[AuditCycle]:
        cycle = await self.find_by_id(audit_cycle_id)
        if cycle is None:
            return None
        cycle.status = "Closed"
        cycle.closed_by = closed_by
        cycle.closed_at = closed_at
        await self.session.flush()
        await self.session.refresh(cycle)
        return cycles
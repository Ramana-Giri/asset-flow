from __future__ import annotations
from datetime import datetime
from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository
from app.db.models.transfer import TransferRequest


class TransferRepository(BaseRepository[TransferRequest]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, TransferRequest)

    async def list_pending(self) -> Sequence[TransferRequest]:
        result = await self.session.execute(
            select(TransferRequest).where(TransferRequest.status == "Requested")
        )
        return result.scalars().all()

    async def list_by_asset(self, asset_id: int) -> Sequence[TransferRequest]:
        result = await self.session.execute(
            select(TransferRequest)
            .where(TransferRequest.asset_id == asset_id)
            .order_by(TransferRequest.created_at.desc())
        )
        return result.scalars().all()

    async def mark_decision(
        self, transfer_id: int, status: str, approved_by: int, approved_at: datetime
    ) -> Optional[TransferRequest]:
        transfer = await self.find_by_id(transfer_id)
        if transfer is None:
            return None
        transfer.status = status
        transfer.approved_by = approved_by
        transfer.approved_at = approved_at
        await self.session.flush()
        await self.session.refresh(transfer)
        return transfer

    async def mark_completed(self, transfer_id: int, new_allocation_id: int) -> Optional[TransferRequest]:
        transfer = await self.find_by_id(transfer_id)
        if transfer is None:
            return None
        transfer.status = "Completed"
        transfer.new_allocation_id = new_allocation_id
        await self.session.flush()
        await self.session.refresh(transfer)
        return transfer
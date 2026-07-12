from __future__ import annotations
from typing import Optional, Sequence

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository
from app.utils.pagination import paginate, PageResult
from app.utils.filters import apply_filters
from app.db.models.asset import Asset
from app.db.models.asset_document import AssetDocument
from app.db.models.asset_status_history import AssetStatusHistory


class AssetRepository(BaseRepository[Asset]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Asset)

    async def find_by_asset_tag(self, asset_tag: str) -> Optional[Asset]:
        result = await self.session.execute(select(Asset).where(Asset.asset_tag == asset_tag))
        return result.scalar_one_or_none()

    async def find_by_serial_number(self, serial_number: str) -> Optional[Asset]:
        result = await self.session.execute(
            select(Asset).where(Asset.serial_number == serial_number)
        )
        return result.scalar_one_or_none()

    async def find_by_qr_code(self, qr_code: str) -> Optional[Asset]:
        result = await self.session.execute(select(Asset).where(Asset.qr_code == qr_code))
        return result.scalar_one_or_none()

    async def search(self, filters: dict, skip: int = 0, limit: int = 50) -> PageResult:
        query = select(Asset)
        text = filters.pop("text", None)
        query = apply_filters(query, Asset, filters)
        if text:
            like = f"%{text}%"
            query = query.where(or_(Asset.name.ilike(like), Asset.asset_tag.ilike(like)))
        return await paginate(self.session, query, skip, limit)

    async def update_status(self, asset_id: int, new_status: str) -> Optional[Asset]:
        asset = await self.find_by_id(asset_id)
        if asset is None:
            return None
        asset.status = new_status
        await self.session.flush()
        await self.session.refresh(asset)
        return asset

    async def add_document(self, asset_id: int, file_url: str, file_type: Optional[str], uploaded_by: Optional[int]) -> AssetDocument:
        doc = AssetDocument(
            asset_id=asset_id, file_url=file_url, file_type=file_type, uploaded_by=uploaded_by
        )
        self.session.add(doc)
        await self.session.flush()
        await self.session.refresh(doc)
        return doc

    async def get_status_history(self, asset_id: int) -> Sequence[AssetStatusHistory]:
        result = await self.session.execute(
            select(AssetStatusHistory)
            .where(AssetStatusHistory.asset_id == asset_id)
            .order_by(AssetStatusHistory.changed_at.desc())
        )
        return result.scalars().all()
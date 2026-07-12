from __future__ import annotations
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository
from app.db.models.asset_category import AssetCategory


class AssetCategoryRepository(BaseRepository[AssetCategory]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, AssetCategory)

    async def find_by_name(self, name: str) -> Optional[AssetCategory]:
        result = await self.session.execute(
            select(AssetCategory).where(AssetCategory.name == name)
        )
        return result.scalar_one_or_none()
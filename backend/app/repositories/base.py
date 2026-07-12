from __future__ import annotations
from typing import Generic, TypeVar, Optional, Sequence

from sqlalchemy import select, func, delete as sa_delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.pagination import paginate, PageResult
from app.utils.filters import apply_filters

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """
    Generic repository providing common CRUD operations for a single
    SQLAlchemy model. Concrete repositories subclass this and add
    entity-specific query methods.
    """

    def __init__(self, session: AsyncSession, model: type[ModelType]):
        self.session = session
        self.model = model

    async def find_by_id(self, id_: int) -> Optional[ModelType]:
        result = await self.session.execute(
            select(self.model).where(self.model.id == id_)
        )
        return result.scalar_one_or_none()

    async def list_all(self, skip: int = 0, limit: int = 50) -> PageResult:
        query = select(self.model)
        return await paginate(self.session, query, skip, limit)

    async def create(self, data: dict) -> ModelType:
        obj = self.model(**data)
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def update(self, id_: int, data: dict) -> Optional[ModelType]:
        obj = await self.find_by_id(id_)
        if obj is None:
            return None
        for key, value in data.items():
            setattr(obj, key, value)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def delete(self, id_: int) -> bool:
        obj = await self.find_by_id(id_)
        if obj is None:
            return False
        await self.session.delete(obj)
        await self.session.flush()
        return True

    async def search(self, filters: dict, skip: int = 0, limit: int = 50) -> PageResult:
        query = select(self.model)
        query = apply_filters(query, self.model, filters)
        return await paginate(self.session, query, skip, limit)
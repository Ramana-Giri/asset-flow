from __future__ import annotations
from typing import Sequence

from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository
from app.db.models.notification import Notification
from app.utils.pagination import paginate, PageResult


class NotificationRepository(BaseRepository[Notification]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Notification)

    async def list_by_user(self, user_id: int, skip: int = 0, limit: int = 50) -> PageResult:
        query = (
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
        )
        return await paginate(self.session, query, skip, limit)

    async def count_unread(self, user_id: int) -> int:
        result = await self.session.execute(
            select(func.count()).select_from(Notification).where(
                Notification.user_id == user_id, Notification.is_read.is_(False)
            )
        )
        return result.scalar_one()

    async def mark_read(self, notification_ids: list[int]) -> int:
        result = await self.session.execute(
            update(Notification)
            .where(Notification.id.in_(notification_ids))
            .values(is_read=True)
        )
        await self.session.flush()
        return result.rowcount
from __future__ import annotations
from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository
from app.utils.pagination import paginate, PageResult
from app.db.models.activity_log import ActivityLog


class ActivityLogRepository(BaseRepository[ActivityLog]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ActivityLog)

    async def create_entry(
        self,
        user_id: Optional[int],
        action: str,
        entity_type: str,
        entity_id: Optional[int] = None,
        details: Optional[dict] = None,
        ip_address: Optional[str] = None,
    ) -> ActivityLog:
        entry = ActivityLog(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details,
            ip_address=ip_address,
        )
        self.session.add(entry)
        await self.session.flush()
        await self.session.refresh(entry)
        return entry

    async def search(
        self,
        user_id: Optional[int] = None,
        entity_type: Optional[str] = None,
        entity_id: Optional[int] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> PageResult:
        query = select(ActivityLog)
        if user_id is not None:
            query = query.where(ActivityLog.user_id == user_id)
        if entity_type is not None:
            query = query.where(ActivityLog.entity_type == entity_type)
        if entity_id is not None:
            query = query.where(ActivityLog.entity_id == entity_id)
        if date_from is not None:
            query = query.where(ActivityLog.created_at >= date_from)
        if date_to is not None:
            query = query.where(ActivityLog.created_at <= date_to)
        query = query.order_by(ActivityLog.created_at.desc())
        return await paginate(self.session, query, skip, limit)
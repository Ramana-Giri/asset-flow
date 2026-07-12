from __future__ import annotations
from datetime import datetime
from typing import Optional

from app.repositories.activity_log_repository import ActivityLogRepository


class ActivityLogService:
    def __init__(self, activity_log_repository: ActivityLogRepository):
        self.activity_logs = activity_log_repository

    async def log(
        self,
        user_id: Optional[int],
        action: str,
        entity_type: str,
        entity_id: Optional[int] = None,
        details: Optional[dict] = None,
        ip_address: Optional[str] = None,
    ) -> None:
        try:
            await self.activity_logs.create_entry(
                user_id=user_id,
                action=action,
                entity_type=entity_type,
                entity_id=entity_id,
                details=details,
                ip_address=ip_address,
            )
        except Exception:
            # Logging must never break the primary business operation.
            pass

    async def search(
        self,
        user_id: Optional[int] = None,
        entity_type: Optional[str] = None,
        entity_id: Optional[int] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 50,
    ):
        return await self.activity_logs.search(
            user_id=user_id,
            entity_type=entity_type,
            entity_id=entity_id,
            date_from=date_from,
            date_to=date_to,
            skip=skip,
            limit=limit,
        )
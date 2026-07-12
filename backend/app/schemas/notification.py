from __future__ import annotations
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    type: str
    title: str
    message: str
    reference_type: Optional[str] = None
    reference_id: Optional[int] = None
    is_read: bool
    created_at: datetime


class NotificationListResponse(BaseModel):
    items: list[NotificationResponse]
    total: int
    skip: int
    limit: int
    unread_count: int = 0


class NotificationMarkReadRequest(BaseModel):
    notification_ids: list[int] = Field(..., min_length=1)
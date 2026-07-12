from __future__ import annotations
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DashboardKPIResponse(BaseModel):
    assets_available: int
    assets_allocated: int
    maintenance_today: int
    active_bookings: int
    pending_transfers: int
    upcoming_returns: int
    overdue_returns: int


class RecentActivityItem(BaseModel):
    id: int
    action: str
    entity_type: str
    entity_id: Optional[int] = None
    user_id: Optional[int] = None
    created_at: datetime


class RecentActivityResponse(BaseModel):
    items: list[RecentActivityItem]
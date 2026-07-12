from __future__ import annotations
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict, model_validator


class BookingCreate(BaseModel):
    asset_id: int
    start_time: datetime
    end_time: datetime
    purpose: Optional[str] = Field(None, max_length=255)
    department_id: Optional[int] = None

    @model_validator(mode="after")
    def check_times(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class BookingReschedule(BaseModel):
    start_time: datetime
    end_time: datetime

    @model_validator(mode="after")
    def check_times(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class BookingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    asset_id: int
    booked_by: int
    department_id: Optional[int] = None
    start_time: datetime
    end_time: datetime
    purpose: Optional[str] = None
    status: str
    cancelled_by: Optional[int] = None
    cancelled_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class BookingListResponse(BaseModel):
    items: list[BookingResponse]
    total: int
    skip: int
    limit: int


class BookingCalendarFilter(BaseModel):
    asset_id: int
    range_start: datetime
    range_end: datetime
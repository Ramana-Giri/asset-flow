from __future__ import annotations
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict, model_validator


class TransferRequestCreate(BaseModel):
    asset_id: int
    to_user_id: Optional[int] = None
    to_department_id: Optional[int] = None
    reason: Optional[str] = None

    @model_validator(mode="after")
    def check_target(self):
        if not self.to_user_id and not self.to_department_id:
            raise ValueError("Either to_user_id or to_department_id must be provided")
        return self


class TransferDecision(BaseModel):
    approve: bool
    rejection_reason: Optional[str] = None


class TransferResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    asset_id: int
    from_allocation_id: Optional[int] = None
    requested_by: int
    to_user_id: Optional[int] = None
    to_department_id: Optional[int] = None
    reason: Optional[str] = None
    status: str
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    new_allocation_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime


class TransferListResponse(BaseModel):
    items: list[TransferResponse]
    total: int
    skip: int
    limit: int


class TransferFilter(BaseModel):
    asset_id: Optional[int] = None
    status: Optional[str] = None
    requested_by: Optional[int] = None
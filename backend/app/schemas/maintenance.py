from __future__ import annotations
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict, model_validator


class MaintenanceRequestCreate(BaseModel):
    asset_id: int
    issue_description: str = Field(..., min_length=1)
    priority: Optional[str] = "Medium"
    photo_url: Optional[str] = Field(None, max_length=500)


class MaintenanceDecision(BaseModel):
    approve: bool
    rejection_reason: Optional[str] = None

    @model_validator(mode="after")
    def check_rejection_reason(self):
        if not self.approve and not self.rejection_reason:
            raise ValueError("rejection_reason is required when rejecting")
        return self


class MaintenanceTechnicianAssign(BaseModel):
    technician_name: str = Field(..., min_length=1, max_length=150)
    technician_contact: Optional[str] = Field(None, max_length=100)


class MaintenanceResolve(BaseModel):
    resolution_notes: Optional[str] = None


class MaintenanceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    asset_id: int
    raised_by: int
    issue_description: str
    priority: str
    photo_url: Optional[str] = None
    status: str
    reviewed_by: Optional[int] = None
    reviewed_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None
    technician_name: Optional[str] = None
    technician_contact: Optional[str] = None
    technician_assigned_at: Optional[datetime] = None
    in_progress_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class MaintenanceListResponse(BaseModel):
    items: list[MaintenanceResponse]
    total: int
    skip: int
    limit: int


class MaintenanceFilter(BaseModel):
    asset_id: Optional[int] = None
    status: Optional[str] = None
    priority: Optional[str] = None
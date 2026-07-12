from __future__ import annotations
from typing import Optional
from datetime import date, datetime

from pydantic import BaseModel, Field, ConfigDict, model_validator


class AuditCycleCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    scope_department_id: Optional[int] = None
    scope_location: Optional[str] = Field(None, max_length=150)
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def check_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")
        return self


class AuditorAssign(BaseModel):
    auditor_ids: list[int] = Field(..., min_length=1)


class AuditItemVerify(BaseModel):
    asset_id: int
    result: str = Field(..., description="Verified, Missing, or Damaged")
    remarks: Optional[str] = None


class AuditDiscrepancyResolve(BaseModel):
    resolution_notes: Optional[str] = None


class AuditCycleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    scope_department_id: Optional[int] = None
    scope_location: Optional[str] = None
    start_date: date
    end_date: date
    status: str
    created_by: int
    closed_by: Optional[int] = None
    closed_at: Optional[datetime] = None
    auditor_ids: list[int] = Field(default_factory=list)
    total_items: int = 0
    verified_count: int = 0
    discrepancy_count: int = 0
    created_at: datetime
    updated_at: datetime


class AuditItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    audit_cycle_id: int
    asset_id: int
    auditor_id: Optional[int] = None
    result: Optional[str] = None
    remarks: Optional[str] = None
    checked_at: Optional[datetime] = None
    resolution_status: str
    resolved_by: Optional[int] = None
    resolved_at: Optional[datetime] = None


class AuditDiscrepancyReportResponse(BaseModel):
    audit_cycle_id: int
    items: list[AuditItemResponse]


class AuditCycleListResponse(BaseModel):
    items: list[AuditCycleResponse]
    total: int
    skip: int
    limit: int
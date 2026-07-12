from __future__ import annotations
from typing import Optional
from datetime import date, datetime

from pydantic import BaseModel, Field, ConfigDict, model_validator


class AllocationCreate(BaseModel):
    asset_id: int
    allocated_to_type: str = Field(..., description="Employee or Department")
    allocated_to_user_id: Optional[int] = None
    allocated_to_department_id: Optional[int] = None
    expected_return_date: Optional[date] = None

    @model_validator(mode="after")
    def check_target(self):
        if self.allocated_to_type == "Employee" and not self.allocated_to_user_id:
            raise ValueError("allocated_to_user_id is required when allocated_to_type is 'Employee'")
        if self.allocated_to_type == "Department" and not self.allocated_to_department_id:
            raise ValueError("allocated_to_department_id is required when allocated_to_type is 'Department'")
        return self


class AllocationReturn(BaseModel):
    return_condition_notes: Optional[str] = None


class AllocationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    asset_id: int
    allocated_to_type: str
    allocated_to_user_id: Optional[int] = None
    allocated_to_department_id: Optional[int] = None
    allocated_by: int
    allocation_date: date
    expected_return_date: Optional[date] = None
    actual_return_date: Optional[date] = None
    return_condition_notes: Optional[str] = None
    returned_by: Optional[int] = None
    status: str
    is_overdue: bool = False
    created_at: datetime
    updated_at: datetime


class AllocationListResponse(BaseModel):
    items: list[AllocationResponse]
    total: int
    skip: int
    limit: int


class AllocationFilter(BaseModel):
    asset_id: Optional[int] = None
    user_id: Optional[int] = None
    department_id: Optional[int] = None
    status: Optional[str] = None
    overdue_only: Optional[bool] = False
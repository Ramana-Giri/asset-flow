from __future__ import annotations
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class DepartmentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    parent_department_id: Optional[int] = None
    head_user_id: Optional[int] = None


class DepartmentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=150)
    parent_department_id: Optional[int] = None
    head_user_id: Optional[int] = None
    status: Optional[str] = None


class DepartmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    parent_department_id: Optional[int] = None
    head_user_id: Optional[int] = None
    status: str
    created_at: datetime
    updated_at: datetime


class DepartmentListResponse(BaseModel):
    items: list[DepartmentResponse]
    total: int
    skip: int
    limit: int


class DepartmentFilter(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    parent_department_id: Optional[int] = None
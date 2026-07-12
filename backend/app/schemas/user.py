from __future__ import annotations
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    department_id: Optional[int] = None


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=150)
    department_id: Optional[int] = None
    status: Optional[str] = None


class UserRoleUpdate(BaseModel):
    role: str = Field(..., description="One of: Admin, Asset Manager, Department Head, Employee")


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    role: str
    department_id: Optional[int] = None
    status: str
    promoted_by: Optional[int] = None
    promoted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class UserListResponse(BaseModel):
    items: list[UserResponse]
    total: int
    skip: int
    limit: int


class UserFilter(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    department_id: Optional[int] = None
    role: Optional[str] = None
    status: Optional[str] = None
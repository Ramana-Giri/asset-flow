from __future__ import annotations
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


class AssetCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    category_id: int
    serial_number: Optional[str] = Field(None, max_length=100)
    acquisition_date: Optional[date] = None
    acquisition_cost: Optional[Decimal] = None
    condition: Optional[str] = "Good"
    location: Optional[str] = Field(None, max_length=150)
    department_id: Optional[int] = None
    is_bookable: bool = False
    custom_field_values: dict = Field(default_factory=dict)


class AssetUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=150)
    condition: Optional[str] = None
    location: Optional[str] = Field(None, max_length=150)
    department_id: Optional[int] = None
    is_bookable: Optional[bool] = None
    custom_field_values: Optional[dict] = None


class AssetDocumentCreate(BaseModel):
    file_type: Optional[str] = Field(None, max_length=50)


class AssetDocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    asset_id: int
    file_url: str
    file_type: Optional[str] = None
    uploaded_by: Optional[int] = None
    uploaded_at: datetime


class AssetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    asset_tag: Optional[str] = None
    name: str
    category_id: int
    serial_number: Optional[str] = None
    acquisition_date: Optional[date] = None
    acquisition_cost: Optional[Decimal] = None
    condition: str
    location: Optional[str] = None
    department_id: Optional[int] = None
    status: str
    is_bookable: bool
    qr_code: Optional[str] = None
    custom_field_values: dict = Field(default_factory=dict)
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime


class AssetListResponse(BaseModel):
    items: list[AssetResponse]
    total: int
    skip: int
    limit: int


class AssetFilter(BaseModel):
    asset_tag: Optional[str] = None
    serial_number: Optional[str] = None
    qr_code: Optional[str] = None
    category_id: Optional[int] = None
    status: Optional[str] = None
    department_id: Optional[int] = None
    location: Optional[str] = None
    is_bookable: Optional[bool] = None
    text: Optional[str] = None


class AssetHistoryResponse(BaseModel):
    asset_id: int
    status_history: list[dict] = Field(default_factory=list)
    allocation_history: list[dict] = Field(default_factory=list)
    maintenance_history: list[dict] = Field(default_factory=list)
from __future__ import annotations
from typing import Optional, Literal
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class CustomFieldDefinition(BaseModel):
    field: str = Field(..., min_length=1, max_length=100)
    type: Literal["string", "number", "boolean", "date"]
    unit: Optional[str] = None
    options: Optional[list[str]] = None


class AssetCategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    custom_field_schema: list[CustomFieldDefinition] = Field(default_factory=list)


class AssetCategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    custom_field_schema: Optional[list[CustomFieldDefinition]] = None


class AssetCategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: Optional[str] = None
    custom_field_schema: list[dict] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


class AssetCategoryListResponse(BaseModel):
    items: list[AssetCategoryResponse]
    total: int
    skip: int
    limit: int
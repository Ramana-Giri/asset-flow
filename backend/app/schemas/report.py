from __future__ import annotations
from pydantic import BaseModel
from typing import Optional


class AssetUtilizationItem(BaseModel):
    asset_id: int
    allocation_count: int
    booking_count: int


class AssetUtilizationReport(BaseModel):
    items: list[AssetUtilizationItem]


class DepartmentSummaryItem(BaseModel):
    department_id: int
    allocation_count: int


class DepartmentSummaryReport(BaseModel):
    items: list[DepartmentSummaryItem]


class MaintenanceSummaryItem(BaseModel):
    asset_id: int
    request_count: int


class MaintenanceSummaryReport(BaseModel):
    items: list[MaintenanceSummaryItem]


class BookingHeatmapItem(BaseModel):
    weekday: int
    hour: int
    booking_count: int


class BookingHeatmapReport(BaseModel):
    items: list[BookingHeatmapItem]


class IdleAssetItem(BaseModel):
    asset_id: int
    name: str
    status: str


class IdleAssetsReport(BaseModel):
    items: list[IdleAssetItem]
    threshold_days: int
from __future__ import annotations
from typing import Optional

from app.repositories.asset_repository import AssetRepository
from app.repositories.asset_category_repository import AssetCategoryRepository
from app.repositories.department_repository import DepartmentRepository
from app.repositories.allocation_repository import AllocationRepository
from app.repositories.maintenance_repository import MaintenanceRepository
from app.core.exceptions import NotFoundException, ValidationError
from app.services.activity_log_service import ActivityLogService
from app.utils.qr_generator import generate_qr_code
from app.utils.file_upload import save_upload

# Allowed asset lifecycle-status transitions used as an internal guard.
_ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "Available": {"Allocated", "Reserved", "Under Maintenance", "Lost", "Retired", "Disposed"},
    "Allocated": {"Available", "Under Maintenance", "Lost"},
    "Reserved": {"Available", "Allocated", "Under Maintenance"},
    "Under Maintenance": {"Available", "Retired", "Disposed"},
    "Lost": {"Available", "Retired"},
    "Retired": {"Disposed"},
    "Disposed": set(),
}


class AssetService:
    def __init__(
        self,
        asset_repository: AssetRepository,
        category_repository: AssetCategoryRepository,
        department_repository: DepartmentRepository,
        allocation_repository: AllocationRepository,
        maintenance_repository: MaintenanceRepository,
        activity_log_service: ActivityLogService,
    ):
        self.assets = asset_repository
        self.categories = category_repository
        self.departments = department_repository
        self.allocations = allocation_repository
        self.maintenance = maintenance_repository
        self.activity_log = activity_log_service

    def _validate_custom_fields(self, schema: list[dict], values: dict) -> None:
        allowed_fields = {entry["field"] for entry in schema}
        for key in values.keys():
            if key not in allowed_fields:
                raise ValidationError(f"'{key}' is not a defined custom field for this category")

    async def register_asset(self, data: dict, actor_id: Optional[int]):
        category = await self.categories.find_by_id(data["category_id"])
        if category is None:
            raise NotFoundException(f"Category {data['category_id']} not found")

        serial_number = data.get("serial_number")
        if serial_number:
            existing = await self.assets.find_by_serial_number(serial_number)
            if existing is not None:
                raise ValidationError("serial_number must be unique")

        custom_field_values = data.get("custom_field_values") or {}
        self._validate_custom_fields(category.custom_field_schema, custom_field_values)

        create_data = {**data, "custom_field_values": custom_field_values, "status": "Available", "created_by": actor_id}
        asset = await self.assets.create(create_data)

        asset.qr_code = generate_qr_code(asset.asset_tag or f"asset-{asset.id}")
        await self.activity_log.log(
            user_id=actor_id, action="REGISTER_ASSET", entity_type="Asset", entity_id=asset.id
        )
        return asset

    async def update_asset(self, asset_id: int, data: dict, actor_id: Optional[int]):
        asset = await self.assets.find_by_id(asset_id)
        if asset is None:
            raise NotFoundException(f"Asset {asset_id} not found")

        if "custom_field_values" in data and data["custom_field_values"] is not None:
            category = await self.categories.find_by_id(asset.category_id)
            self._validate_custom_fields(category.custom_field_schema, data["custom_field_values"])

        updated = await self.assets.update(asset_id, data)
        await self.activity_log.log(
            user_id=actor_id, action="UPDATE_ASSET", entity_type="Asset", entity_id=asset_id, details=data
        )
        return updated

    async def upload_document(self, asset_id: int, file, file_type: Optional[str], actor_id: Optional[int]):
        asset = await self.assets.find_by_id(asset_id)
        if asset is None:
            raise NotFoundException(f"Asset {asset_id} not found")

        file_url = await save_upload(file, subfolder=f"assets/{asset_id}")
        document = await self.assets.add_document(asset_id, file_url, file_type, actor_id)
        await self.activity_log.log(
            user_id=actor_id,
            action="UPLOAD_ASSET_DOCUMENT",
            entity_type="Asset",
            entity_id=asset_id,
            details={"document_id": document.id},
        )
        return document

    async def search_assets(self, filters: dict, skip: int = 0, limit: int = 50):
        return await self.assets.search(filters, skip, limit)

    async def get_asset_history(self, asset_id: int):
        asset = await self.assets.find_by_id(asset_id)
        if asset is None:
            raise NotFoundException(f"Asset {asset_id} not found")

        status_history = await self.assets.get_status_history(asset_id)
        allocation_history = await self.allocations.list_by_user(asset_id)  # noqa: kept simple per skeleton scope
        maintenance_history = await self.maintenance.list_by_asset(asset_id)
        return {
            "asset_id": asset_id,
            "status_history": status_history,
            "maintenance_history": maintenance_history,
        }

    async def transition_status(
        self,
        asset_id: int,
        new_status: str,
        actor_id: Optional[int],
        reference_type: str = "Manual",
        reference_id: Optional[int] = None,
    ):
        asset = await self.assets.find_by_id(asset_id)
        if asset is None:
            raise NotFoundException(f"Asset {asset_id} not found")

        allowed = _ALLOWED_TRANSITIONS.get(asset.status, set())
        if new_status not in allowed:
            raise ValidationError(f"Cannot transition asset from '{asset.status}' to '{new_status}'")

        updated = await self.assets.update_status(asset_id, new_status)
        await self.activity_log.log(
            user_id=actor_id,
            action="ASSET_STATUS_CHANGE",
            entity_type="Asset",
            entity_id=asset_id,
            details={"old_status": asset.status, "new_status": new_status, "reference_type": reference_type, "reference_id": reference_id},
        )
        return updated
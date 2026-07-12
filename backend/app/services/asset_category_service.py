from __future__ import annotations
from sqlalchemy import select

from app.repositories.asset_category_repository import AssetCategoryRepository
from app.db.models.asset import Asset
from app.core.exceptions import NotFoundException, ValidationError
from app.services.activity_log_service import ActivityLogService
from sqlalchemy.ext.asyncio import AsyncSession


class AssetCategoryService:
    def __init__(
        self,
        session: AsyncSession,
        category_repository: AssetCategoryRepository,
        activity_log_service: ActivityLogService,
    ):
        self.session = session
        self.categories = category_repository
        self.activity_log = activity_log_service

    async def list_categories(self, skip: int = 0, limit: int = 50):
        return await self.categories.list_all(skip, limit)

    async def get_category(self, category_id: int):
        category = await self.categories.find_by_id(category_id)
        if category is None:
            raise NotFoundException(f"Category {category_id} not found")
        return category

    def _validate_schema(self, custom_field_schema: list[dict]) -> None:
        for entry in custom_field_schema:
            if "field" not in entry or "type" not in entry:
                raise ValidationError("Each custom_field_schema entry requires 'field' and 'type'")

    async def create_category(self, name: str, description: str | None, custom_field_schema: list[dict], actor_id: int):
        existing = await self.categories.find_by_name(name)
        if existing is not None:
            raise ValidationError("Category name must be unique")
        self._validate_schema(custom_field_schema)

        category = await self.categories.create(
            {"name": name, "description": description, "custom_field_schema": custom_field_schema}
        )
        await self.activity_log.log(
            user_id=actor_id, action="CREATE_ASSET_CATEGORY", entity_type="AssetCategory", entity_id=category.id
        )
        return category

    async def update_category(self, category_id: int, data: dict, actor_id: int):
        if "name" in data and data["name"]:
            existing = await self.categories.find_by_name(data["name"])
            if existing is not None and existing.id != category_id:
                raise ValidationError("Category name must be unique")
        if "custom_field_schema" in data and data["custom_field_schema"] is not None:
            self._validate_schema(data["custom_field_schema"])

        category = await self.categories.update(category_id, data)
        if category is None:
            raise NotFoundException(f"Category {category_id} not found")
        await self.activity_log.log(
            user_id=actor_id,
            action="UPDATE_ASSET_CATEGORY",
            entity_type="AssetCategory",
            entity_id=category_id,
            details=data,
        )
        return category

    async def delete_category(self, category_id: int, actor_id: int):
        result = await self.session.execute(select(Asset).where(Asset.category_id == category_id).limit(1))
        if result.scalar_one_or_none() is not None:
            raise ValidationError("Cannot delete a category that still has assets registered under it")

        deleted = await self.categories.delete(category_id)
        if not deleted:
            raise NotFoundException(f"Category {category_id} not found")
        await self.activity_log.log(
            user_id=actor_id, action="DELETE_ASSET_CATEGORY", entity_type="AssetCategory", entity_id=category_id
        )
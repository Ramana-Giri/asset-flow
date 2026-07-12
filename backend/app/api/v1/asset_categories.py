from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_asset_manager
from app.core.responses import success
from app.repositories.asset_category_repository import AssetCategoryRepository
from app.repositories.activity_log_repository import ActivityLogRepository
from app.services.asset_category_service import AssetCategoryService
from app.services.activity_log_service import ActivityLogService
from app.schemas.asset_category import AssetCategoryCreate, AssetCategoryUpdate

router = APIRouter(prefix="/asset-categories", tags=["Asset Categories"])


def get_category_service(db: AsyncSession = Depends(get_db)) -> AssetCategoryService:
    return AssetCategoryService(db, AssetCategoryRepository(db), ActivityLogService(ActivityLogRepository(db)))


@router.get("")
async def list_categories(skip: int = 0, limit: int = 50, service: AssetCategoryService = Depends(get_category_service)):
    page = await service.list_categories(skip, limit)
    return success(data={"items": page.items, "total": page.total, "skip": page.skip, "limit": page.limit})


@router.get("/{category_id}")
async def get_category(category_id: int, service: AssetCategoryService = Depends(get_category_service)):
    category = await service.get_category(category_id)
    return success(data=category)


@router.post("")
async def create_category(
    payload: AssetCategoryCreate, service: AssetCategoryService = Depends(get_category_service), manager=Depends(get_current_asset_manager)
):
    schema_dicts = [f.model_dump() for f in payload.custom_field_schema]
    category = await service.create_category(payload.name, payload.description, schema_dicts, manager.id)
    return success(data=category, message="Category created")


@router.put("/{category_id}")
async def update_category(
    category_id: int,
    payload: AssetCategoryUpdate,
    service: AssetCategoryService = Depends(get_category_service),
    manager=Depends(get_current_asset_manager),
):
    data = payload.model_dump(exclude_none=True)
    if "custom_field_schema" in data:
        data["custom_field_schema"] = [f if isinstance(f, dict) else f.model_dump() for f in data["custom_field_schema"]]
    category = await service.update_category(category_id, data, manager.id)
    return success(data=category, message="Category updated")


@router.delete("/{category_id}")
async def delete_category(
    category_id: int, service: AssetCategoryService = Depends(get_category_service), manager=Depends(get_current_asset_manager)
):
    await service.delete_category(category_id, manager.id)
    return success(message="Category deleted")
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user, get_current_asset_manager
from app.core.responses import success
from app.repositories.asset_repository import AssetRepository
from app.repositories.asset_category_repository import AssetCategoryRepository
from app.repositories.department_repository import DepartmentRepository
from app.repositories.allocation_repository import AllocationRepository
from app.repositories.maintenance_repository import MaintenanceRepository
from app.repositories.activity_log_repository import ActivityLogRepository
from app.services.asset_service import AssetService
from app.services.activity_log_service import ActivityLogService
from app.schemas.asset import AssetCreate, AssetUpdate, AssetFilter

router = APIRouter(prefix="/assets", tags=["Assets"])


def get_asset_service(db: AsyncSession = Depends(get_db)) -> AssetService:
    return AssetService(
        AssetRepository(db),
        AssetCategoryRepository(db),
        DepartmentRepository(db),
        AllocationRepository(db),
        MaintenanceRepository(db),
        ActivityLogService(ActivityLogRepository(db)),
    )


@router.get("")
async def search_assets(
    filters: AssetFilter = Depends(), skip: int = 0, limit: int = 50, service: AssetService = Depends(get_asset_service)
):
    page = await service.search_assets(filters.model_dump(exclude_none=True), skip, limit)
    return success(data={"items": page.items, "total": page.total, "skip": page.skip, "limit": page.limit})


@router.get("/{asset_id}")
async def get_asset(asset_id: int, service: AssetService = Depends(get_asset_service)):
    page = await service.search_assets({}, skip=0, limit=1)
    asset = next((a for a in page.items if a.id == asset_id), None)
    return success(data=asset)


@router.post("")
async def register_asset(
    payload: AssetCreate, service: AssetService = Depends(get_asset_service), actor=Depends(get_current_asset_manager)
):
    asset = await service.register_asset(payload.model_dump(exclude_none=True), actor.id)
    return success(data=asset, message="Asset registered")


@router.put("/{asset_id}")
async def update_asset(
    asset_id: int, payload: AssetUpdate, service: AssetService = Depends(get_asset_service), actor=Depends(get_current_user)
):
    asset = await service.update_asset(asset_id, payload.model_dump(exclude_none=True), actor.id)
    return success(data=asset, message="Asset updated")


@router.post("/{asset_id}/documents")
async def upload_document(
    asset_id: int,
    file: UploadFile = File(...),
    file_type: str = Form(None),
    service: AssetService = Depends(get_asset_service),
    actor=Depends(get_current_user),
):
    document = await service.upload_document(asset_id, file, file_type, actor.id)
    return success(data=document, message="Document uploaded")


@router.get("/{asset_id}/history")
async def get_asset_history(asset_id: int, service: AssetService = Depends(get_asset_service)):
    history = await service.get_asset_history(asset_id)
    return success(data=history)
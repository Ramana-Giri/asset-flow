from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.dependencies import get_db, require_role, get_current_user
from app.models.user import User
from app.models.assets import Asset
from app.models.enums import AssetStatus
from pydantic import BaseModel
from typing import Optional, List
from datetime import date

router = APIRouter(prefix="/assets", tags=["Assets"])

class AssetCreate(BaseModel):
    name: str
    category_id: int
    serial_number: Optional[str] = None
    acquisition_date: Optional[date] = None
    acquisition_cost: Optional[float] = None
    condition: str = "Good"
    location: Optional[str] = None
    department_id: Optional[int] = None
    is_bookable: bool = False
    custom_field_values: dict = {}

class AssetOut(BaseModel):
    id: int
    asset_tag: Optional[str]
    name: str
    category_id: int
    serial_number: Optional[str]
    status: str
    department_id: Optional[int]
    is_bookable: bool

    class Config:
        from_attributes = True

@router.post("/", response_model=AssetOut)
def create_asset(data: AssetCreate, db: Session = Depends(get_db),
                 current_user: User = Depends(require_role("Asset Manager","Admin"))):
    asset = Asset(**data.model_dump(), created_by=current_user.id, status=AssetStatus.Available)
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset

@router.get("/", response_model=List[AssetOut])
def search_assets(
    status: Optional[str] = None,
    category_id: Optional[int] = None,
    department_id: Optional[int] = None,
    is_bookable: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Asset)
    if status:
        query = query.filter(Asset.status == status)
    if category_id:
        query = query.filter(Asset.category_id == category_id)
    if department_id:
        query = query.filter(Asset.department_id == department_id)
    if is_bookable is not None:
        query = query.filter(Asset.is_bookable == is_bookable)
    return query.all()
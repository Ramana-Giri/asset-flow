from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from app.dependencies import get_db, get_current_user, require_role
from app.models.user import User
from app.services.allocation_service import allocate_asset, return_asset

router = APIRouter(prefix="/allocations", tags=["Allocations"])

@router.post("/")
def create_allocation(
    asset_id: int,
    target_type: str,
    target_id: int,
    expected_return_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Asset Manager","Admin"))
):
    alloc = allocate_asset(db, asset_id, current_user.id, target_type, target_id, expected_return_date)
    return {"msg": "Asset allocated", "allocation_id": alloc.id}

@router.post("/{allocation_id}/return")
def return_asset_endpoint(
    allocation_id: int,
    condition_notes: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    alloc = return_asset(db, allocation_id, current_user.id, condition_notes)
    return {"msg": "Asset returned", "allocation_id": alloc.id}
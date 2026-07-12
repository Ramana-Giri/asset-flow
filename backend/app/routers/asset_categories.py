from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, require_role
from app.models.user import User
from app.models.asset_category import AssetCategory
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter(prefix="/categories", tags=["Asset Categories"])

class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    custom_field_schema: Optional[list] = []

class CategoryOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    custom_field_schema: list

    class Config:
        from_attributes = True

@router.post("/", response_model=CategoryOut)
def create_category(data: CategoryCreate, db: Session = Depends(get_db),
                    current_user: User = Depends(require_role("Admin"))):
    if db.query(AssetCategory).filter_by(name=data.name).first():
        raise HTTPException(400, "Category already exists")
    cat = AssetCategory(**data.model_dump())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

@router.get("/", response_model=List[CategoryOut])
def list_categories(db: Session = Depends(get_db),
                    current_user: User = Depends(require_role("Admin","Asset Manager","Department Head","Employee"))):
    return db.query(AssetCategory).all()
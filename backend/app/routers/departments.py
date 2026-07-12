from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.dependencies import get_current_user, require_role
from app.models.user import User
from app.models.department import Department
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/departments", tags=["Departments"])

class DepartmentCreate(BaseModel):
    name: str
    parent_department_id: Optional[int] = None
    head_user_id: Optional[int] = None

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    parent_department_id: Optional[int] = None
    head_user_id: Optional[int] = None

class DepartmentOut(BaseModel):
    id: int
    name: str
    parent_department_id: Optional[int]
    head_user_id: Optional[int]

    class Config:
        from_attributes = True

@router.post("/", response_model=DepartmentOut)
def create_department(
    data: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):
    if db.query(Department).filter(Department.name == data.name).first():
        raise HTTPException(status_code=400, detail="Department already exists")
    dept = Department(**data.model_dump())
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return dept

@router.get("/", response_model=List[DepartmentOut])
def list_departments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Department).all()

@router.get("/{department_id}", response_model=DepartmentOut)
def get_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dept = db.query(Department).get(department_id)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return dept

@router.put("/{department_id}", response_model=DepartmentOut)
def update_department(
    department_id: int,
    data: DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):
    dept = db.query(Department).get(department_id)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(dept, field, value)
    db.commit()
    db.refresh(dept)
    return dept

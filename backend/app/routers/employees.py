from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.dependencies import get_db, require_role, get_current_user
from app.models.user import User
from app.models.enums import UserRole
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/employees", tags=["Employee Directory"])

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str
    department_id: Optional[int]
    status: str

    class Config:
        from_attributes = True

@router.get("/", response_model=List[UserOut])
def list_employees(db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    return db.query(User).all()

@router.put("/{user_id}/promote")
def promote_employee(user_id: int, new_role: UserRole,
                     db: Session = Depends(get_db),
                     admin: User = Depends(require_role("Admin"))):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    if new_role not in [UserRole.Department_Head, UserRole.Asset_Manager]:
        raise HTTPException(400, "Can only promote to Department Head or Asset Manager")
    user.role = new_role
    user.promoted_by = admin.id
    user.promoted_at = func.now()
    db.commit()
    return {"msg": f"User promoted to {new_role.value}"}
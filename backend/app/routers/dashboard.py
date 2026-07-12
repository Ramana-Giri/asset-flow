from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_current_user, get_db
from app.models.user import User
from sqlalchemy import text

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/kpis")
def get_kpis(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM v_dashboard_kpis")).fetchone()
    if result:
        return dict(result._mapping)
    return {}

@router.get("/overdue-returns")
def overdue_returns(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.execute(text("SELECT * FROM v_overdue_allocations")).fetchall()
    return [dict(row._mapping) for row in rows]
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.assets import Asset
from app.models.enums import AssetStatus

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/asset-status-summary")
def asset_status_summary(db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    from sqlalchemy import func
    results = db.query(Asset.status, func.count(Asset.id)).group_by(Asset.status).all()
    return [{"status": s.value, "count": c} for s, c in results]
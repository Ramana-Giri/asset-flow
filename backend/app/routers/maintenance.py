from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user, require_role
from app.models.user import User
from app.models.maintenance_request import MaintenanceRequest
from app.models.assets import Asset
from app.models.enums import MaintenanceStatus, AssetStatus
from pydantic import BaseModel

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])

class MaintenanceCreate(BaseModel):
    asset_id: int
    issue_description: str
    priority: str = "Medium"
    photo_url: str = None

@router.post("/")
def raise_request(data: MaintenanceCreate,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    req = MaintenanceRequest(asset_id=data.asset_id, raised_by=current_user.id,
                             issue_description=data.issue_description,
                             priority=data.priority, photo_url=data.photo_url)
    db.add(req)
    db.commit()
    return {"msg": "Maintenance request raised", "id": req.id}

@router.put("/{request_id}/approve")
def approve(request_id: int, db: Session = Depends(get_db),
            current_user: User = Depends(require_role("Asset Manager","Admin"))):
    req = db.query(MaintenanceRequest).get(request_id)
    if not req or req.status != MaintenanceStatus.Pending:
        raise HTTPException(404, "Invalid request")
    req.status = MaintenanceStatus.Approved
    req.reviewed_by = current_user.id
    req.reviewed_at = func.now()
    asset = db.query(Asset).get(req.asset_id)
    asset.status = AssetStatus.Under_Maintenance
    db.commit()
    return {"msg": "Approved, asset status updated"}

@router.put("/{request_id}/resolve")
def resolve(request_id: int, resolution_notes: str = None,
            db: Session = Depends(get_db),
            current_user: User = Depends(require_role("Asset Manager","Admin"))):
    req = db.query(MaintenanceRequest).get(request_id)
    if not req or req.status not in [MaintenanceStatus.Approved, MaintenanceStatus.In_Progress]:
        raise HTTPException(400, "Invalid state")
    req.status = MaintenanceStatus.Resolved
    req.resolved_at = func.now()
    req.resolution_notes = resolution_notes
    asset = db.query(Asset).get(req.asset_id)
    asset.status = AssetStatus.Available
    db.commit()
    return {"msg": "Resolved, asset available"}
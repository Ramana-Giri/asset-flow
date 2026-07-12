from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user, require_role
from app.models.user import User
from app.models.audit_cycle import AuditCycle
from app.models.audit_item import AuditItem
from app.models.assets import Asset
from app.models.enums import AuditCycleStatus
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/audits", tags=["Audits"])

class AuditCreate(BaseModel):
    name: str
    scope_department_id: Optional[int] = None
    scope_location: Optional[str] = None
    start_date: date
    end_date: date

@router.post("/cycles")
def create_cycle(data: AuditCreate, db: Session = Depends(get_db),
                 current_user: User = Depends(require_role("Admin"))):
    cycle = AuditCycle(**data.model_dump(), created_by=current_user.id)
    db.add(cycle)
    db.commit()
    return {"msg": "Audit cycle created", "id": cycle.id}

@router.post("/cycles/{cycle_id}/start")
def start_cycle(cycle_id: int, db: Session = Depends(get_db),
                current_user: User = Depends(require_role("Admin"))):
    cycle = db.query(AuditCycle).get(cycle_id)
    if not cycle or cycle.status != AuditCycleStatus.Planned:
        raise HTTPException(400, "Invalid cycle")
    # generate audit items for assets in scope
    query = db.query(Asset)
    if cycle.scope_department_id:
        query = query.filter(Asset.department_id == cycle.scope_department_id)
    if cycle.scope_location:
        query = query.filter(Asset.location == cycle.scope_location)
    assets = query.all()
    for asset in assets:
        db.add(AuditItem(audit_cycle_id=cycle_id, asset_id=asset.id))
    cycle.status = AuditCycleStatus.In_Progress
    db.commit()
    return {"msg": f"Cycle started, {len(assets)} assets added"}

@router.put("/items/{item_id}")
def verify_item(item_id: int, result: str, remarks: str = None,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    item = db.query(AuditItem).get(item_id)
    if not item:
        raise HTTPException(404, "Item not found")
    item.result = result
    item.remarks = remarks
    item.auditor_id = current_user.id
    item.checked_at = func.now()
    db.commit()
    return {"msg": "Item verified"}

@router.post("/cycles/{cycle_id}/close")
def close_cycle(cycle_id: int, db: Session = Depends(get_db),
                current_user: User = Depends(require_role("Admin"))):
    cycle = db.query(AuditCycle).get(cycle_id)
    if not cycle or cycle.status != AuditCycleStatus.In_Progress:
        raise HTTPException(400, "Invalid cycle")
    # auto-update asset statuses for missing items
    missing_items = db.query(AuditItem).filter_by(audit_cycle_id=cycle_id, result="Missing").all()
    for item in missing_items:
        asset = db.query(Asset).get(item.asset_id)
        if asset:
            asset.status = "Lost"
    cycle.status = AuditCycleStatus.Closed
    cycle.closed_by = current_user.id
    cycle.closed_at = func.now()
    db.commit()
    return {"msg": "Cycle closed", "missing_assets": len(missing_items)}
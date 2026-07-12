from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user, require_role
from app.models.user import User
from app.models.transfer_request import TransferRequest
from app.models.allocations import Allocation
from app.models.assets import Asset
from app.models.enums import TransferStatus, AllocationStatus, AssetStatus
from pydantic import BaseModel

router = APIRouter(prefix="/transfers", tags=["Transfers"])

class TransferRequestIn(BaseModel):
    asset_id: int
    from_allocation_id: int
    to_user_id: int = None
    to_department_id: int = None
    reason: str = None

@router.post("/request")
def request_transfer(data: TransferRequestIn,
                     db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    # ensure asset is allocated
    alloc = db.query(Allocation).filter_by(id=data.from_allocation_id, status=AllocationStatus.Active).first()
    if not alloc:
        raise HTTPException(400, "Invalid active allocation")
    req = TransferRequest(asset_id=data.asset_id, from_allocation_id=data.from_allocation_id,
                          requested_by=current_user.id, to_user_id=data.to_user_id,
                          to_department_id=data.to_department_id, reason=data.reason)
    db.add(req)
    db.commit()
    return {"msg": "Transfer requested", "id": req.id}

@router.put("/{transfer_id}/approve")
def approve_transfer(transfer_id: int,
                     db: Session = Depends(get_db),
                     current_user: User = Depends(require_role("Asset Manager","Department Head"))):
    transfer = db.query(TransferRequest).get(transfer_id)
    if not transfer or transfer.status != TransferStatus.Requested:
        raise HTTPException(404, "Transfer not found")
    # close old allocation
    old_alloc = db.query(Allocation).get(transfer.from_allocation_id)
    old_alloc.status = AllocationStatus.Returned
    old_alloc.actual_return_date = func.current_date()
    # create new allocation
    new_alloc = Allocation(
        asset_id=transfer.asset_id,
        allocated_to_type="Employee" if transfer.to_user_id else "Department",
        allocated_to_user_id=transfer.to_user_id,
        allocated_to_department_id=transfer.to_department_id,
        allocated_by=current_user.id,
        status=AllocationStatus.Active
    )
    db.add(new_alloc)
    db.flush()
    transfer.status = TransferStatus.Completed
    transfer.approved_by = current_user.id
    transfer.approved_at = func.now()
    transfer.new_allocation_id = new_alloc.id
    asset = db.query(Asset).get(transfer.asset_id)
    asset.status = AssetStatus.Allocated
    db.commit()
    return {"msg": "Transfer approved, new allocation created"}
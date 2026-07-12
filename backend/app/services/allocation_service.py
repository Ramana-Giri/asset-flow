from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.assets import Asset
from app.models.allocations import Allocation
from app.models.user import User
from app.models.department import Department
from app.models.enums import AllocationStatus, AssetStatus

def allocate_asset(db: Session, asset_id: int, allocator_id: int, target_type: str,
                   target_id: int, expected_return_date=None):
    asset = db.query(Asset).get(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    if asset.status != AssetStatus.Available:
        raise HTTPException(status_code=400, detail=f"Asset not available (current status: {asset.status.value})")
    
    # Build allocation
    alloc = Allocation(
        asset_id=asset_id,
        allocated_to_type=target_type,
        allocated_to_user_id=target_id if target_type == "Employee" else None,
        allocated_to_department_id=target_id if target_type == "Department" else None,
        allocated_by=allocator_id,
        expected_return_date=expected_return_date,
        status=AllocationStatus.Active
    )
    db.add(alloc)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # Fetch who currently holds it
        active_alloc = db.query(Allocation).filter(
            Allocation.asset_id == asset_id,
            Allocation.status == AllocationStatus.Active
        ).first()
        if active_alloc:
            holder = active_alloc.allocated_to_user.name if active_alloc.allocated_to_user else active_alloc.department.name
            raise HTTPException(status_code=409, detail=f"Asset is already allocated to {holder}. Request a transfer instead.")
        else:
            raise HTTPException(status_code=500, detail="Allocation conflict")
    
    # Update asset status to Allocated
    asset.status = AssetStatus.Allocated
    db.commit()
    return alloc

def return_asset(db: Session, allocation_id: int, returned_by: int, condition_notes: str = None):
    alloc = db.query(Allocation).get(allocation_id)
    if not alloc or alloc.status != AllocationStatus.Active:
        raise HTTPException(status_code=404, detail="Active allocation not found")
    alloc.status = AllocationStatus.Returned
    alloc.actual_return_date = func.current_date()
    alloc.returned_by = returned_by
    alloc.return_condition_notes = condition_notes
    asset = db.query(Asset).get(alloc.asset_id)
    asset.status = AssetStatus.Available
    db.commit()
    return alloc
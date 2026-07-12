from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.resource_booking import ResourceBooking
from app.models.assets import Asset
from app.models.enums import BookingStatus
from app.services.booking_service import has_overlap

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/")
def create_booking(asset_id: int, start_time: datetime, end_time: datetime,
                   purpose: str = None, department_id: int = None,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    asset = db.query(Asset).get(asset_id)
    if not asset or not asset.is_bookable:
        raise HTTPException(400, "Asset not bookable")
    if has_overlap(db, asset_id, start_time, end_time):
        raise HTTPException(409, "Time slot overlaps with an existing booking")
    booking = ResourceBooking(
        asset_id=asset_id,
        booked_by=current_user.id,
        department_id=department_id or current_user.department_id,
        start_time=start_time,
        end_time=end_time,
        purpose=purpose,
        status=BookingStatus.Upcoming
    )
    db.add(booking)
    db.commit()
    return {"msg": "Booking created", "id": booking.id}
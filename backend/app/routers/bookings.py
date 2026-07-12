from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List
from app.dependencies import get_db, get_current_user, require_role
from app.models.user import User
from app.models.resource_booking import ResourceBooking
from app.models.assets import Asset
from app.models.enums import BookingStatus
from app.services.booking_service import has_overlap
from pydantic import BaseModel

router = APIRouter(prefix="/bookings", tags=["Bookings"])

class BookingCreate(BaseModel):
    asset_id: int
    start_time: datetime
    end_time: datetime
    purpose: Optional[str] = None
    department_id: Optional[int] = None

class BookingOut(BaseModel):
    id: int
    asset_id: int
    booked_by: int
    start_time: datetime
    end_time: datetime
    purpose: Optional[str]
    status: BookingStatus
    created_at: datetime

    class Config:
        from_attributes = True

@router.post("/", response_model=BookingOut)
def create_booking(
    data: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    asset = db.query(Asset).get(data.asset_id)
    if not asset or not asset.is_bookable:
        raise HTTPException(400, "Asset not bookable")
    if data.end_time <= data.start_time:
        raise HTTPException(400, "End time must be after start time")
    if has_overlap(db, data.asset_id, data.start_time, data.end_time):
        raise HTTPException(409, "Time slot overlaps with an existing booking")

    booking = ResourceBooking(
        asset_id=data.asset_id,
        booked_by=current_user.id,
        department_id=data.department_id or current_user.department_id,
        start_time=data.start_time,
        end_time=data.end_time,
        purpose=data.purpose,
        status=BookingStatus.Upcoming
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

@router.get("/", response_model=List[BookingOut])
def get_bookings(
    asset_id: Optional[int] = Query(None),
    status: Optional[BookingStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(ResourceBooking)
    if asset_id:
        query = query.filter(ResourceBooking.asset_id == asset_id)
    if status:
        query = query.filter(ResourceBooking.status == status)
    # Optional: only show future/present bookings, you can add a date filter
    bookings = query.order_by(ResourceBooking.start_time).all()
    return bookings

@router.put("/{booking_id}/cancel")
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = db.query(ResourceBooking).get(booking_id)
    if not booking:
        raise HTTPException(404, "Booking not found")
    if booking.status not in [BookingStatus.Upcoming, BookingStatus.Ongoing]:
        raise HTTPException(400, "Only upcoming/ongoing bookings can be cancelled")
    booking.status = BookingStatus.Cancelled
    booking.cancelled_by = current_user.id
    booking.cancelled_at = datetime.utcnow()
    db.commit()
    return {"msg": "Booking cancelled"}

class RescheduleRequest(BaseModel):
    start_time: datetime
    end_time: datetime

@router.put("/{booking_id}/reschedule")
def reschedule_booking(
    booking_id: int,
    data: RescheduleRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = db.query(ResourceBooking).get(booking_id)
    if not booking:
        raise HTTPException(404, "Booking not found")
    if booking.status not in [BookingStatus.Upcoming, BookingStatus.Ongoing]:
        raise HTTPException(400, "Only upcoming/ongoing bookings can be rescheduled")
    if data.end_time <= data.start_time:
        raise HTTPException(400, "End time must be after start time")
    # Check overlap (exclude current booking)
    if has_overlap(db, booking.asset_id, data.start_time, data.end_time, exclude_id=booking_id):
        raise HTTPException(409, "New time slot overlaps with another booking")
    booking.start_time = data.start_time
    booking.end_time = data.end_time
    db.commit()
    return {"msg": "Booking rescheduled"}
from sqlalchemy.orm import Session
from app.models.resource_booking import ResourceBooking

def has_overlap(db: Session, asset_id: int, start, end, exclude_id=None):
    overlapping = db.query(ResourceBooking).filter(
        ResourceBooking.asset_id == asset_id,
        ResourceBooking.status.in_(["Upcoming", "Ongoing"]),
        ResourceBooking.start_time < end,
        ResourceBooking.end_time > start,
    )
    if exclude_id:
        overlapping = overlapping.filter(ResourceBooking.id != exclude_id)
    return overlapping.first() is not None
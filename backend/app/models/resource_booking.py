from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Enum
from sqlalchemy.sql import func
from app.database import Base
from app.models.enums import BookingStatus

class ResourceBooking(Base):
    __tablename__ = "resource_bookings"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    booked_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    purpose = Column(String(255))
    status = Column(Enum(BookingStatus), default=BookingStatus.Upcoming, nullable=False)
    cancelled_by = Column(Integer, ForeignKey("users.id"))
    cancelled_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
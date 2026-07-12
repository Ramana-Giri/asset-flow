from __future__ import annotations
from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, ForeignKey, DateTime, String, CheckConstraint, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.core.enums import BookingStatus

# NOTE: the GiST EXCLUDE constraint (excl_no_overlapping_bookings) uses
# btree_gist + tstzrange() and is not expressible via SQLAlchemy's
# CheckConstraint; it is created by the raw assetflow_schema.sql migration
# (see alembic/versions/0001_initial.py) rather than declared here.


class ResourceBooking(Base):
    __tablename__ = "resource_bookings"
    __table_args__ = (
        CheckConstraint("end_time > start_time", name="chk_booking_time"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"), nullable=False)
    booked_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    purpose: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[BookingStatus] = mapped_column(
        postgresql.ENUM(
            "Upcoming", "Ongoing", "Completed", "Cancelled",
            name="booking_status", create_type=False,
        ),
        nullable=False,
        server_default="Upcoming",
    )
    cancelled_by: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    cancelled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    asset: Mapped["Asset"] = relationship("Asset", back_populates="bookings")
    booked_by_user: Mapped["User"] = relationship(
        "User", back_populates="bookings", foreign_keys=[booked_by]
    )
    department: Mapped[Optional["Department"]] = relationship("Department", foreign_keys=[department_id])
    cancelled_by_user: Mapped[Optional["User"]] = relationship("User", foreign_keys=[cancelled_by])
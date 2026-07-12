from __future__ import annotations
from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, ForeignKey, DateTime, String, Text, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.core.enums import MaintenancePriority, MaintenanceStatus


class MaintenanceRequest(Base):
    __tablename__ = "maintenance_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"), nullable=False)
    raised_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    issue_description: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[MaintenancePriority] = mapped_column(
        postgresql.ENUM(
            "Low", "Medium", "High", "Critical",
            name="maintenance_priority", create_type=False,
        ),
        nullable=False,
        server_default="Medium",
    )
    photo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    status: Mapped[MaintenanceStatus] = mapped_column(
        postgresql.ENUM(
            "Pending", "Approved", "Rejected", "Technician Assigned",
            "In Progress", "Resolved",
            name="maintenance_status", create_type=False,
        ),
        nullable=False,
        server_default="Pending",
    )
    reviewed_by: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    rejection_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    technician_name: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    technician_contact: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    technician_assigned_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    in_progress_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    resolution_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    asset: Mapped["Asset"] = relationship("Asset", back_populates="maintenance_requests")
    raised_by_user: Mapped["User"] = relationship(
        "User", back_populates="maintenance_requests_raised", foreign_keys=[raised_by]
    )
    reviewed_by_user: Mapped[Optional["User"]] = relationship("User", foreign_keys=[reviewed_by])
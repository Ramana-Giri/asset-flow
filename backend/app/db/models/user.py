from __future__ import annotations
from datetime import datetime
from typing import Optional, List

from sqlalchemy import String, Integer, ForeignKey, DateTime, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.core.enums import UserRole, AccountStatus


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        postgresql.ENUM(
            "Admin", "Asset Manager", "Department Head", "Employee",
            name="user_role", create_type=False,
        ),
        nullable=False,
        server_default="Employee",
    )
    department_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("departments.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[AccountStatus] = mapped_column(
        postgresql.ENUM("Active", "Inactive", name="account_status", create_type=False),
        nullable=False,
        server_default="Active",
    )
    promoted_by: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    promoted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    department: Mapped[Optional["Department"]] = relationship(
        "Department", back_populates="users", foreign_keys=[department_id]
    )
    promoted_by_user: Mapped[Optional["User"]] = relationship(
        "User", remote_side=[id], foreign_keys=[promoted_by]
    )
    sessions: Mapped[List["UserSession"]] = relationship("UserSession", back_populates="user")
    password_reset_tokens: Mapped[List["PasswordResetToken"]] = relationship(
        "PasswordResetToken", back_populates="user"
    )
    allocations_received: Mapped[List["Allocation"]] = relationship(
        "Allocation", back_populates="allocated_to_user", foreign_keys="Allocation.allocated_to_user_id"
    )
    allocations_made: Mapped[List["Allocation"]] = relationship(
        "Allocation", back_populates="allocated_by_user", foreign_keys="Allocation.allocated_by"
    )
    maintenance_requests_raised: Mapped[List["MaintenanceRequest"]] = relationship(
        "MaintenanceRequest", back_populates="raised_by_user", foreign_keys="MaintenanceRequest.raised_by"
    )
    bookings: Mapped[List["ResourceBooking"]] = relationship(
        "ResourceBooking", back_populates="booked_by_user", foreign_keys="ResourceBooking.booked_by"
    )
    notifications: Mapped[List["Notification"]] = relationship("Notification", back_populates="user")
    activity_logs: Mapped[List["ActivityLog"]] = relationship("ActivityLog", back_populates="user")
from __future__ import annotations
from datetime import datetime, date
from typing import Optional, List

from sqlalchemy import Integer, ForeignKey, DateTime, Date, Text, CheckConstraint, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.core.enums import AllocationTarget, AllocationStatus


class Allocation(Base):
    __tablename__ = "allocations"
    __table_args__ = (
        CheckConstraint(
            "(allocated_to_type = 'Employee' AND allocated_to_user_id IS NOT NULL "
            "AND allocated_to_department_id IS NULL) OR "
            "(allocated_to_type = 'Department' AND allocated_to_department_id IS NOT NULL "
            "AND allocated_to_user_id IS NULL)",
            name="chk_allocation_target",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"), nullable=False)
    allocated_to_type: Mapped[AllocationTarget] = mapped_column(
        postgresql.ENUM("Employee", "Department", name="allocation_target", create_type=False),
        nullable=False,
    )
    allocated_to_user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    allocated_to_department_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("departments.id"), nullable=True
    )
    allocated_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    allocation_date: Mapped[date] = mapped_column(Date, nullable=False, server_default=func.current_date())
    expected_return_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    actual_return_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    return_condition_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    returned_by: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    status: Mapped[AllocationStatus] = mapped_column(
        postgresql.ENUM("Active", "Returned", name="allocation_status", create_type=False),
        nullable=False,
        server_default="Active",
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    asset: Mapped["Asset"] = relationship("Asset", back_populates="allocations")
    allocated_to_user: Mapped[Optional["User"]] = relationship(
        "User", back_populates="allocations_received", foreign_keys=[allocated_to_user_id]
    )
    allocated_to_department: Mapped[Optional["Department"]] = relationship(
        "Department", foreign_keys=[allocated_to_department_id]
    )
    allocated_by_user: Mapped["User"] = relationship(
        "User", back_populates="allocations_made", foreign_keys=[allocated_by]
    )
    returned_by_user: Mapped[Optional["User"]] = relationship("User", foreign_keys=[returned_by])
    transfer_requests_from: Mapped[List["TransferRequest"]] = relationship(
        "TransferRequest", back_populates="from_allocation", foreign_keys="TransferRequest.from_allocation_id"
    )
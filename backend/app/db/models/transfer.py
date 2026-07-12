from __future__ import annotations
from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, ForeignKey, DateTime, Text, CheckConstraint, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.core.enums import TransferStatus


class TransferRequest(Base):
    __tablename__ = "transfer_requests"
    __table_args__ = (
        CheckConstraint(
            "to_user_id IS NOT NULL OR to_department_id IS NOT NULL",
            name="chk_transfer_target",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"), nullable=False)
    from_allocation_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("allocations.id"), nullable=True
    )
    requested_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    to_user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    to_department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[TransferStatus] = mapped_column(
        postgresql.ENUM(
            "Requested", "Approved", "Rejected", "Completed",
            name="transfer_status", create_type=False,
        ),
        nullable=False,
        server_default="Requested",
    )
    approved_by: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    new_allocation_id: Mapped[Optional[int]] = mapped_column(ForeignKey("allocations.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    asset: Mapped["Asset"] = relationship("Asset", back_populates="transfer_requests")
    from_allocation: Mapped[Optional["Allocation"]] = relationship(
        "Allocation", back_populates="transfer_requests_from", foreign_keys=[from_allocation_id]
    )
    new_allocation: Mapped[Optional["Allocation"]] = relationship(
        "Allocation", foreign_keys=[new_allocation_id]
    )
    requested_by_user: Mapped["User"] = relationship("User", foreign_keys=[requested_by])
    approved_by_user: Mapped[Optional["User"]] = relationship("User", foreign_keys=[approved_by])
    to_user: Mapped[Optional["User"]] = relationship("User", foreign_keys=[to_user_id])
    to_department: Mapped[Optional["Department"]] = relationship(
        "Department", foreign_keys=[to_department_id]
    )
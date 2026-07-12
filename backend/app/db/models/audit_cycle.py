from __future__ import annotations
from datetime import datetime, date
from typing import Optional, List

from sqlalchemy import Integer, ForeignKey, DateTime, Date, String, CheckConstraint, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.core.enums import AuditCycleStatus


class AuditCycle(Base):
    __tablename__ = "audit_cycles"
    __table_args__ = (
        CheckConstraint("end_date >= start_date", name="chk_audit_dates"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    scope_department_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("departments.id"), nullable=True
    )
    scope_location: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[AuditCycleStatus] = mapped_column(
        postgresql.ENUM(
            "Planned", "In Progress", "Closed",
            name="audit_cycle_status", create_type=False,
        ),
        nullable=False,
        server_default="Planned",
    )
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    closed_by: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    scope_department: Mapped[Optional["Department"]] = relationship(
        "Department", foreign_keys=[scope_department_id]
    )
    created_by_user: Mapped["User"] = relationship("User", foreign_keys=[created_by])
    closed_by_user: Mapped[Optional["User"]] = relationship("User", foreign_keys=[closed_by])
    auditors: Mapped[List["AuditCycleAuditor"]] = relationship(
        "AuditCycleAuditor", back_populates="audit_cycle", cascade="all, delete-orphan"
    )
    items: Mapped[List["AuditItem"]] = relationship(
        "AuditItem", back_populates="audit_cycle", cascade="all, delete-orphan"
    )
from __future__ import annotations
from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, ForeignKey, DateTime, Text, UniqueConstraint, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.core.enums import AuditResult, ResolutionStatus


class AuditItem(Base):
    __tablename__ = "audit_items"
    __table_args__ = (
        UniqueConstraint("audit_cycle_id", "asset_id", name="uq_audit_item_cycle_asset"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    audit_cycle_id: Mapped[int] = mapped_column(
        ForeignKey("audit_cycles.id", ondelete="CASCADE"), nullable=False
    )
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"), nullable=False)
    auditor_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    result: Mapped[Optional[AuditResult]] = mapped_column(
        postgresql.ENUM("Verified", "Missing", "Damaged", name="audit_result", create_type=False),
        nullable=True,
    )
    remarks: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    checked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    resolution_status: Mapped[ResolutionStatus] = mapped_column(
        postgresql.ENUM("Open", "Resolved", name="resolution_status", create_type=False),
        nullable=False,
        server_default="Open",
    )
    resolved_by: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    audit_cycle: Mapped["AuditCycle"] = relationship("AuditCycle", back_populates="items")
    asset: Mapped["Asset"] = relationship("Asset", back_populates="audit_items")
    auditor: Mapped[Optional["User"]] = relationship("User", foreign_keys=[auditor_id])
    resolved_by_user: Mapped[Optional["User"]] = relationship("User", foreign_keys=[resolved_by])
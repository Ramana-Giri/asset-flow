from __future__ import annotations
from datetime import datetime

from sqlalchemy import Integer, ForeignKey, DateTime, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class AuditCycleAuditor(Base):
    __tablename__ = "audit_cycle_auditors"
    __table_args__ = (
        UniqueConstraint("audit_cycle_id", "auditor_id", name="uq_audit_cycle_auditor"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    audit_cycle_id: Mapped[int] = mapped_column(
        ForeignKey("audit_cycles.id", ondelete="CASCADE"), nullable=False
    )
    auditor_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    assigned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    audit_cycle: Mapped["AuditCycle"] = relationship("AuditCycle", back_populates="auditors")
    auditor: Mapped["User"] = relationship("User", foreign_keys=[auditor_id])
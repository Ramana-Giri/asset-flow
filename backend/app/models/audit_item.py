from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum, Text
from sqlalchemy.sql import func
from app.database import Base
from app.models.enums import AuditResult, ResolutionStatus

class AuditItem(Base):
    __tablename__ = "audit_items"

    id = Column(Integer, primary_key=True, index=True)
    audit_cycle_id = Column(Integer, ForeignKey("audit_cycles.id", ondelete="CASCADE"), nullable=False)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    auditor_id = Column(Integer, ForeignKey("users.id"))
    result = Column(Enum(AuditResult))
    remarks = Column(Text)
    checked_at = Column(DateTime(timezone=True))
    resolution_status = Column(Enum(ResolutionStatus), default=ResolutionStatus.Open, nullable=False)
    resolved_by = Column(Integer, ForeignKey("users.id"))
    resolved_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
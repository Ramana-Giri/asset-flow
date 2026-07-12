
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum, Text
from sqlalchemy.sql import func
from app.database import Base
from app.models.enums import TransferStatus

class TransferRequest(Base):
    __tablename__ = "transfer_requests"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    from_allocation_id = Column(Integer, ForeignKey("allocations.id"))
    requested_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    to_user_id = Column(Integer, ForeignKey("users.id"))
    to_department_id = Column(Integer, ForeignKey("departments.id"))
    reason = Column(Text)
    status = Column(Enum(TransferStatus), default=TransferStatus.Requested, nullable=False)
    approved_by = Column(Integer, ForeignKey("users.id"))
    approved_at = Column(DateTime(timezone=True))
    new_allocation_id = Column(Integer, ForeignKey("allocations.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
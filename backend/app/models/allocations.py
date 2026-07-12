from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Enum, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.enums import AllocationTarget, AllocationStatus

class Allocation(Base):
    __tablename__ = "allocations"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    allocated_to_type = Column(Enum(AllocationTarget), nullable=False)
    allocated_to_user_id = Column(Integer, ForeignKey("users.id"))
    allocated_to_department_id = Column(Integer, ForeignKey("departments.id"))
    allocated_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    allocation_date = Column(Date, default=func.current_date())
    expected_return_date = Column(Date)
    actual_return_date = Column(Date)
    return_condition_notes = Column(Text)
    returned_by = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum(AllocationStatus), default=AllocationStatus.Active, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    asset = relationship("Asset")
    allocated_to_user = relationship("User", foreign_keys=[allocated_to_user_id])
    allocated_to_department = relationship("Department", foreign_keys=[allocated_to_department_id])
    allocator = relationship("User", foreign_keys=[allocated_by])
    returner = relationship("User", foreign_keys=[returned_by])
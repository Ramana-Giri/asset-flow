from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.enums import AccountStatus

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True, nullable=False)
    parent_department_id = Column(Integer, ForeignKey("departments.id", ondelete="SET NULL"))
    head_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    status = Column(Enum(AccountStatus), default=AccountStatus.Active, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    parent = relationship("Department", remote_side=[id], backref="sub_departments")
    head = relationship("User", foreign_keys=[head_user_id], back_populates="headed_department")
    members = relationship("User", back_populates="department", foreign_keys="User.department_id")
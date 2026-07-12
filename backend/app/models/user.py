from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.enums import UserRole, AccountStatus

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.Employee, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id", ondelete="SET NULL"))
    status = Column(Enum(AccountStatus), default=AccountStatus.Active, nullable=False)
    promoted_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    promoted_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    department = relationship("Department", back_populates="members", foreign_keys=[department_id])
    headed_department = relationship("Department", back_populates="head", foreign_keys="Department.head_user_id")
    promoted_by_user = relationship("User", remote_side=[id], backref="promoted_users")
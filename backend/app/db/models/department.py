from __future__ import annotations
from datetime import datetime
from typing import Optional, List

from sqlalchemy import String, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects import postgresql

from app.db.base import Base
from app.core.enums import AccountStatus


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    parent_department_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("departments.id", ondelete="SET NULL"), nullable=True
    )
    head_user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[AccountStatus] = mapped_column(
        postgresql.ENUM("Active", "Inactive", name="account_status", create_type=False),
        nullable=False,
        server_default="Active",
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    parent: Mapped[Optional["Department"]] = relationship(
        "Department", remote_side=[id], foreign_keys=[parent_department_id], back_populates="children"
    )
    children: Mapped[List["Department"]] = relationship(
        "Department", back_populates="parent", foreign_keys=[parent_department_id]
    )
    head: Mapped[Optional["User"]] = relationship(
        "User", foreign_keys=[head_user_id], viewonly=True
    )
    users: Mapped[List["User"]] = relationship(
        "User", back_populates="department", foreign_keys="User.department_id"
    )
    assets: Mapped[List["Asset"]] = relationship("Asset", back_populates="department")
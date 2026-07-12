"""
Department Model  (table: "departments")

Purpose
-------
Organizational unit; supports optional parent-child hierarchy and an assigned Department Head.

Responsibilities
-----------------
- Maps ORM attributes 1:1 to the "departments" table defined in assetflow_schema.sql.
- Declares relationships to related entities for ORM (lazy) navigation.
- Contains NO business logic, NO validation logic, NO query logic.

Interacts With
--------------
- db/base.py -> inherits the shared DeclarativeBase.
- repositories/*_repository.py -> the only layer permitted to query/persist Department directly.
- SQLAlchemy relationship()s mirror the FKs declared in assetflow_schema.sql.

NOTE: This file is a structural skeleton only. Method/function bodies are
intentionally left as `pass` (no business logic / SQL / validation code),
per generation scope. Docstrings describe what each piece IS responsible
for once implemented.
"""
"""Department Model (table: "departments")"""

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import ENUM as PGEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import AccountStatus
from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.asset import Asset
    from app.db.models.user import User

_account_status_enum = PGEnum(
    AccountStatus, name="account_status", create_type=False, values_callable=lambda obj: [e.value for e in obj]
)


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    parent_department_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("departments.id", ondelete="SET NULL"), nullable=True
    )
    head_user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[AccountStatus] = mapped_column(_account_status_enum, nullable=False, default=AccountStatus.ACTIVE)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    parent: Mapped[Optional["Department"]] = relationship(
        "Department", remote_side=[id], foreign_keys=[parent_department_id], back_populates="children"
    )
    children: Mapped[List["Department"]] = relationship(
        "Department", foreign_keys=[parent_department_id], back_populates="parent"
    )
    head: Mapped[Optional["User"]] = relationship(
        "User", foreign_keys=[head_user_id], back_populates="headed_department"
    )
    users: Mapped[List["User"]] = relationship(
        "User", foreign_keys="User.department_id", back_populates="department"
    )
    assets: Mapped[List["Asset"]] = relationship("Asset", back_populates="department")
"""
User Model  (table: "users")

Purpose
-------
Employee directory + authentication identity. Signup always creates role=Employee; only Admin promotes to Department Head / Asset Manager.

Responsibilities
-----------------
- Maps ORM attributes 1:1 to the "users" table defined in assetflow_schema.sql.
- Declares relationships to related entities for ORM (lazy) navigation.
- Contains NO business logic, NO validation logic, NO query logic.

Interacts With
--------------
- db/base.py -> inherits the shared DeclarativeBase.
- repositories/*_repository.py -> the only layer permitted to query/persist User directly.
- SQLAlchemy relationship()s mirror the FKs declared in assetflow_schema.sql.

NOTE: This file is a structural skeleton only. Method/function bodies are
intentionally left as `pass` (no business logic / SQL / validation code),
per generation scope. Docstrings describe what each piece IS responsible
for once implemented.
"""
"""User Model (table: "users")"""

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import ENUM as PGEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import AccountStatus, UserRole
from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.activity_log import ActivityLog
    from app.db.models.allocation import Allocation
    from app.db.models.booking import ResourceBooking
    from app.db.models.department import Department
    from app.db.models.maintenance import MaintenanceRequest
    from app.db.models.notification import Notification
    from app.db.models.password_reset import PasswordResetToken
    from app.db.models.session import UserSession

_user_role_enum = PGEnum(
    UserRole, name="user_role", create_type=False, values_callable=lambda obj: [e.value for e in obj]
)
_account_status_enum = PGEnum(
    AccountStatus, name="account_status", create_type=False, values_callable=lambda obj: [e.value for e in obj]
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(_user_role_enum, nullable=False, default=UserRole.EMPLOYEE)
    department_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("departments.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[AccountStatus] = mapped_column(_account_status_enum, nullable=False, default=AccountStatus.ACTIVE)
    promoted_by: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    promoted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    department: Mapped[Optional["Department"]] = relationship(
        "Department", foreign_keys=[department_id], back_populates="users"
    )
    headed_department: Mapped[Optional["Department"]] = relationship(
        "Department", foreign_keys="Department.head_user_id", back_populates="head", uselist=False
    )
    promoted_by_user: Mapped[Optional["User"]] = relationship(
        "User", remote_side=[id], foreign_keys=[promoted_by]
    )

    sessions: Mapped[List["UserSession"]] = relationship("UserSession", back_populates="user")
    password_reset_tokens: Mapped[List["PasswordResetToken"]] = relationship(
        "PasswordResetToken", back_populates="user"
    )
    allocations_received: Mapped[List["Allocation"]] = relationship(
        "Allocation", foreign_keys="Allocation.allocated_to_user_id", back_populates="allocated_to_user"
    )
    allocations_made: Mapped[List["Allocation"]] = relationship(
        "Allocation", foreign_keys="Allocation.allocated_by", back_populates="allocated_by_user"
    )
    maintenance_requests_raised: Mapped[List["MaintenanceRequest"]] = relationship(
        "MaintenanceRequest", foreign_keys="MaintenanceRequest.raised_by", back_populates="raised_by_user"
    )
    bookings: Mapped[List["ResourceBooking"]] = relationship(
        "ResourceBooking", foreign_keys="ResourceBooking.booked_by", back_populates="booked_by_user"
    )
    notifications: Mapped[List["Notification"]] = relationship("Notification", back_populates="user")
    activity_logs: Mapped[List["ActivityLog"]] = relationship("ActivityLog", back_populates="user")
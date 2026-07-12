from __future__ import annotations
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List

from sqlalchemy import String, Integer, ForeignKey, DateTime, Date, Numeric, Boolean, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.core.enums import AssetCondition, AssetStatus


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    asset_tag: Mapped[Optional[str]] = mapped_column(String(20), unique=True, nullable=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("asset_categories.id"), nullable=False)
    serial_number: Mapped[Optional[str]] = mapped_column(String(100), unique=True, nullable=True)
    acquisition_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    acquisition_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2), nullable=True)
    condition: Mapped[AssetCondition] = mapped_column(
        postgresql.ENUM(
            "Excellent", "Good", "Fair", "Poor", "Damaged",
            name="asset_condition", create_type=False,
        ),
        nullable=False,
        server_default="Good",
    )
    location: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("departments.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[AssetStatus] = mapped_column(
        postgresql.ENUM(
            "Available", "Allocated", "Reserved", "Under Maintenance",
            "Lost", "Retired", "Disposed",
            name="asset_status", create_type=False,
        ),
        nullable=False,
        server_default="Available",
    )
    is_bookable: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    qr_code: Mapped[Optional[str]] = mapped_column(String(150), unique=True, nullable=True)
    custom_field_values: Mapped[dict] = mapped_column(JSONB, nullable=False, server_default="{}")
    created_by: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    category: Mapped["AssetCategory"] = relationship("AssetCategory", back_populates="assets")
    department: Mapped[Optional["Department"]] = relationship("Department", back_populates="assets")
    created_by_user: Mapped[Optional["User"]] = relationship("User", foreign_keys=[created_by])
    documents: Mapped[List["AssetDocument"]] = relationship(
        "AssetDocument", back_populates="asset", cascade="all, delete-orphan"
    )
    status_history: Mapped[List["AssetStatusHistory"]] = relationship(
        "AssetStatusHistory", back_populates="asset", cascade="all, delete-orphan"
    )
    allocations: Mapped[List["Allocation"]] = relationship("Allocation", back_populates="asset")
    transfer_requests: Mapped[List["TransferRequest"]] = relationship(
        "TransferRequest", back_populates="asset"
    )
    bookings: Mapped[List["ResourceBooking"]] = relationship("ResourceBooking", back_populates="asset")
    maintenance_requests: Mapped[List["MaintenanceRequest"]] = relationship(
        "MaintenanceRequest", back_populates="asset"
    )
    audit_items: Mapped[List["AuditItem"]] = relationship("AuditItem", back_populates="asset")
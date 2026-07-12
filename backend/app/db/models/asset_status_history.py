from __future__ import annotations
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Integer, ForeignKey, DateTime, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.core.enums import AssetStatus

_ASSET_STATUS_ENUM = postgresql.ENUM(
    "Available", "Allocated", "Reserved", "Under Maintenance",
    "Lost", "Retired", "Disposed",
    name="asset_status", create_type=False,
)


class AssetStatusHistory(Base):
    __tablename__ = "asset_status_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id", ondelete="CASCADE"), nullable=False)
    old_status: Mapped[Optional[AssetStatus]] = mapped_column(_ASSET_STATUS_ENUM, nullable=True)
    new_status: Mapped[AssetStatus] = mapped_column(_ASSET_STATUS_ENUM, nullable=False)
    changed_by: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    reason: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    reference_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    reference_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    asset: Mapped["Asset"] = relationship("Asset", back_populates="status_history")
    changed_by_user: Mapped[Optional["User"]] = relationship("User", foreign_keys=[changed_by])
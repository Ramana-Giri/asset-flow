from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from app.database import Base
from app.models.enums import AssetStatus

class AssetStatusHistory(Base):
    __tablename__ = "asset_status_history"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id", ondelete="CASCADE"), nullable=False)
    old_status = Column(Enum(AssetStatus))
    new_status = Column(Enum(AssetStatus), nullable=False)
    changed_by = Column(Integer, ForeignKey("users.id"))
    reason = Column(String(255))
    reference_type = Column(String(50))
    reference_id = Column(Integer)
    changed_at = Column(DateTime(timezone=True), server_default=func.now())
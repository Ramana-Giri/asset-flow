from sqlalchemy import Column, Integer, String, Date, Numeric, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.database import Base
from app.models.enums import AssetCondition, AssetStatus

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    asset_tag = Column(String(20), unique=True)
    name = Column(String(150), nullable=False)
    category_id = Column(Integer, ForeignKey("asset_categories.id"), nullable=False)
    serial_number = Column(String(100), unique=True)
    acquisition_date = Column(Date)
    acquisition_cost = Column(Numeric(12,2))
    condition = Column(Enum(AssetCondition), default=AssetCondition.Good, nullable=False)
    location = Column(String(150))
    department_id = Column(Integer, ForeignKey("departments.id", ondelete="SET NULL"))
    status = Column(Enum(AssetStatus), default=AssetStatus.Available, nullable=False)
    is_bookable = Column(Boolean, default=False, nullable=False)
    qr_code = Column(String(150), unique=True)
    custom_field_values = Column(JSONB, default=dict, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
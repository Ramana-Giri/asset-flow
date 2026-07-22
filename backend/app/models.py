from sqlalchemy import Integer, String, Column, ForeignKey, CheckConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email_address = Column(String(255), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)


class Asset(Base):
    __tablename__ = "assets"

    asset_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    status = Column(String(255), nullable=False, default="not assigned")
    assigned_to = Column(Integer, ForeignKey("employees.employee_id"), nullable=True)

    __table_args__ = (
        CheckConstraint(
            "status IN ('assigned', 'not assigned')", name="check_status_valid_values"
        ),
    )

"""
Application Enums

Purpose
-------
Python-side mirrors of every PostgreSQL ENUM TYPE declared in assetflow_schema.sql, for use in models, schemas, and services.

Responsibilities
-----------------
- Declare one Python `enum.Enum` (or `StrEnum`) per SQL ENUM TYPE, with identical member values.
- Serve as the single source of truth for valid string values across the app layer (mirroring, not replacing, the DB-level ENUM constraint).

Interacts With
--------------
- db/models/*.py -> SQLAlchemy Enum columns reference these.
- schemas/*.py -> Pydantic fields reference these for validation.
- services/*.py -> status-transition logic compares against these.

NOTE: This file is a structural skeleton only. Method/function bodies are
intentionally left as `pass` (no business logic / SQL / validation code),
per generation scope. Docstrings describe what each piece IS responsible
for once implemented.
"""

from enum import Enum


class UserRole(str, Enum):
    """Mirrors SQL type user_role."""
    ADMIN = "Admin"
    ASSET_MANAGER = "Asset Manager"
    DEPARTMENT_HEAD = "Department Head"
    EMPLOYEE = "Employee"


class AccountStatus(str, Enum):
    """Mirrors SQL type account_status."""
    ACTIVE = "Active"
    INACTIVE = "Inactive"


class AssetCondition(str, Enum):
    """Mirrors SQL type asset_condition."""
    EXCELLENT = "Excellent"
    GOOD = "Good"
    FAIR = "Fair"
    POOR = "Poor"
    DAMAGED = "Damaged"


class AssetStatus(str, Enum):
    """Mirrors SQL type asset_status."""
    AVAILABLE = "Available"
    ALLOCATED = "Allocated"
    RESERVED = "Reserved"
    UNDER_MAINTENANCE = "Under Maintenance"
    LOST = "Lost"
    RETIRED = "Retired"
    DISPOSED = "Disposed"


class AllocationTarget(str, Enum):
    """Mirrors SQL type allocation_target."""
    EMPLOYEE = "Employee"
    DEPARTMENT = "Department"


class AllocationStatus(str, Enum):
    """Mirrors SQL type allocation_status."""
    ACTIVE = "Active"
    RETURNED = "Returned"


class TransferStatus(str, Enum):
    """Mirrors SQL type transfer_status."""
    REQUESTED = "Requested"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    COMPLETED = "Completed"


class BookingStatus(str, Enum):
    """Mirrors SQL type booking_status."""
    UPCOMING = "Upcoming"
    ONGOING = "Ongoing"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class MaintenancePriority(str, Enum):
    """Mirrors SQL type maintenance_priority."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class MaintenanceStatus(str, Enum):
    """Mirrors SQL type maintenance_status."""
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    TECHNICIAN_ASSIGNED = "Technician Assigned"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"


class AuditCycleStatus(str, Enum):
    """Mirrors SQL type audit_cycle_status."""
    PLANNED = "Planned"
    IN_PROGRESS = "In Progress"
    CLOSED = "Closed"


class AuditResult(str, Enum):
    """Mirrors SQL type audit_result."""
    VERIFIED = "Verified"
    MISSING = "Missing"
    DAMAGED = "Damaged"


class ResolutionStatus(str, Enum):
    """Mirrors SQL type resolution_status."""
    OPEN = "Open"
    RESOLVED = "Resolved"

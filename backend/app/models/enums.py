import enum

class UserRole(str, enum.Enum):
    Admin = "Admin"
    Asset_Manager = "Asset Manager"
    Department_Head = "Department Head"
    Employee = "Employee"

class AccountStatus(str, enum.Enum):
    Active = "Active"
    Inactive = "Inactive"

class AssetCondition(str, enum.Enum):
    Excellent = "Excellent"
    Good = "Good"
    Fair = "Fair"
    Poor = "Poor"
    Damaged = "Damaged"

class AssetStatus(str, enum.Enum):
    Available = "Available"
    Allocated = "Allocated"
    Reserved = "Reserved"
    Under_Maintenance = "Under Maintenance"
    Lost = "Lost"
    Retired = "Retired"
    Disposed = "Disposed"

class AllocationTarget(str, enum.Enum):
    Employee = "Employee"
    Department = "Department"

class AllocationStatus(str, enum.Enum):
    Active = "Active"
    Returned = "Returned"

class TransferStatus(str, enum.Enum):
    Requested = "Requested"
    Approved = "Approved"
    Rejected = "Rejected"
    Completed = "Completed"

class BookingStatus(str, enum.Enum):
    Upcoming = "Upcoming"
    Ongo = "Ongoing"
    Completed = "Completed"
    Cancelled = "Cancelled"

class MaintenancePriority(str, enum.Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"
    Critical = "Critical"

class MaintenanceStatus(str, enum.Enum):
    Pending = "Pending"
    Approved = "Approved"
    Rejected = "Rejected"
    Technician_Assigned = "Technician Assigned"
    In_Progress = "In Progress"
    Resolved = "Resolved"

class AuditCycleStatus(str, enum.Enum):
    Planned = "Planned"
    In_Progress = "In Progress"
    Closed = "Closed"

class AuditResult(str, enum.Enum):
    Verified = "Verified"
    Missing = "Missing"
    Damaged = "Damaged"

class ResolutionStatus(str, enum.Enum):
    Open = "Open"
    Resolved = "Resolved"
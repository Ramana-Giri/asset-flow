"""
Application Constants

Purpose
-------
Named constants to avoid magic strings scattered across services/routers.

Responsibilities
-----------------
- ASSET_TAG_PREFIX, notification type strings, activity-log action strings, pagination defaults, etc.

Interacts With
--------------
- services/*.py -> reference these instead of hardcoded literals.
"""

# --- Pagination ---
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# --- Asset ---
ASSET_TAG_PREFIX = "AF-"  # actual generation happens in the DB trigger; kept here for reference/tests

# --- Notification types (see requirements Screen 10) ---
NOTIFICATION_TYPES = (
    "Asset Assigned",
    "Maintenance Approved",
    "Maintenance Rejected",
    "Maintenance Resolved",
    "Booking Confirmed",
    "Booking Cancelled",
    "Booking Reminder",
    "Transfer Approved",
    "Overdue Return Alert",
    "Audit Discrepancy Flagged",
)

# --- Activity log actions ---
# Grouped by the service module that emits them. Every literal action string
# referenced in a services/*.py docstring is represented here; the generic
# CRUD-style actions (create/update/activate/deactivate on User, Department,
# AssetCategory) are included too even though those services describe their
# steps as "write ActivityLog" rather than naming an exact literal, so the
# whole app has one shared vocabulary instead of each service inventing its
# own string at implementation time.
ACTIVITY_ACTIONS = (
    # --- Auth (auth_service.py) ---
    "SIGNUP",
    "LOGIN",
    "LOGOUT",
    "FORGOT_PASSWORD_REQUESTED",
    "PASSWORD_RESET",

    # --- Users (user_service.py) ---
    "CREATE_USER",
    "UPDATE_USER",
    "SET_USER_DEPARTMENT",
    "PROMOTE_USER",
    "ACTIVATE_USER",
    "DEACTIVATE_USER",

    # --- Departments (department_service.py) ---
    "CREATE_DEPARTMENT",
    "UPDATE_DEPARTMENT",
    "ASSIGN_DEPARTMENT_HEAD",
    "DEACTIVATE_DEPARTMENT",

    # --- Asset categories (asset_category_service.py) ---
    "CREATE_ASSET_CATEGORY",
    "UPDATE_ASSET_CATEGORY",
    "DELETE_ASSET_CATEGORY",

    # --- Assets (asset_service.py) ---
    "REGISTER_ASSET",
    "UPDATE_ASSET",
    "UPLOAD_ASSET_DOCUMENT",
    "CHANGE_ASSET_STATUS",

    # --- Allocations (allocation_service.py) ---
    "ALLOCATE_ASSET",
    "RETURN_ASSET",

    # --- Transfers (transfer_service.py) ---
    "REQUEST_TRANSFER",
    "APPROVE_TRANSFER",
    "REJECT_TRANSFER",

    # --- Bookings (booking_service.py) ---
    "CREATE_BOOKING",
    "CANCEL_BOOKING",
    "RESCHEDULE_BOOKING",

    # --- Maintenance (maintenance_service.py) ---
    "RAISE_MAINTENANCE_REQUEST",
    "APPROVE_MAINTENANCE",
    "REJECT_MAINTENANCE",
    "RESOLVE_MAINTENANCE",

    # --- Audits (audit_service.py) ---
    "CREATE_AUDIT_CYCLE",
    "ASSIGN_AUDITORS",
    "VERIFY_AUDIT_ASSET",
    "RESOLVE_AUDIT_DISCREPANCY",
    "CLOSE_AUDIT_CYCLE",
)
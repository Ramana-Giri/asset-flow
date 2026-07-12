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

NOTE: This file is a structural skeleton only. Method/function bodies are
intentionally left as `pass` (no business logic / SQL / validation code),
per generation scope. Docstrings describe what each piece IS responsible
for once implemented.
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

# --- Activity log actions (non-exhaustive; extend per module) ---
ACTIVITY_ACTIONS = (
    "SIGNUP", "LOGIN", "LOGOUT", "PASSWORD_RESET",
    "PROMOTE_USER", "REGISTER_ASSET", "ALLOCATE_ASSET", "RETURN_ASSET",
    "REQUEST_TRANSFER", "APPROVE_TRANSFER", "REJECT_TRANSFER",
    "CREATE_BOOKING", "CANCEL_BOOKING", "RESCHEDULE_BOOKING",
    "RAISE_MAINTENANCE_REQUEST", "APPROVE_MAINTENANCE", "REJECT_MAINTENANCE",
    "RESOLVE_MAINTENANCE", "CREATE_AUDIT_CYCLE", "ASSIGN_AUDITORS",
    "VERIFY_AUDIT_ASSET", "RESOLVE_AUDIT_DISCREPANCY", "CLOSE_AUDIT_CYCLE",
)

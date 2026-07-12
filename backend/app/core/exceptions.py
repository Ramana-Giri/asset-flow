"""
Domain Exceptions

Purpose
-------
Custom exception classes thrown by Services on business-rule violations. Routers catch these and convert them into HTTP responses; repositories never raise these.

Responsibilities
-----------------
- Declare one exception per domain rule violation named in the architecture guide.
- register_exception_handlers(app): map each exception type to an HTTP status + core/responses.py envelope.

Interacts With
--------------
- services/*.py -> raises these on rule violations.
- main.py -> registers the exception handlers that translate these to HTTP responses.
- core/responses.py -> error envelope shape reused by the handlers.

NOTE: This file is a structural skeleton only. Method/function bodies are
intentionally left as `pass` (no business logic / SQL / validation code),
per generation scope. Docstrings describe what each piece IS responsible
for once implemented.
"""

class AssetFlowException(Exception):
    """Base class for all domain exceptions in this application."""
    pass


class NotFoundException(AssetFlowException):
    """Raised when a requested entity does not exist."""
    pass


class PermissionDenied(AssetFlowException):
    """Raised when the current user lacks the required role/permission."""
    pass


class AssetAlreadyAllocated(AssetFlowException):
    """
    Raised when attempting to allocate an asset that already has an
    Active allocation. Should carry enough context (current holder) for
    the router to surface "currently held by <name>" plus a Transfer
    Request suggestion, per the Allocation screen requirements.
    """
    pass


class BookingOverlapException(AssetFlowException):
    """Raised when a requested booking time range overlaps an existing Upcoming/Ongoing booking for the same resource."""
    pass


class TransferNotAllowed(AssetFlowException):
    """Raised when a transfer request is invalid (e.g. no active allocation, invalid target, wrong approver)."""
    pass


class MaintenanceAlreadyOpen(AssetFlowException):
    """Raised when raising a maintenance request for an asset that already has a non-terminal maintenance request open."""
    pass


class DepartmentInactive(AssetFlowException):
    """Raised when an operation targets a Department with status='Inactive' that requires an Active department."""
    pass


class CircularDepartmentHierarchy(AssetFlowException):
    """Raised when a department update would create a circular parent/child relationship."""
    pass


class ValidationError(AssetFlowException):
    """Raised for cross-field business validation failures not expressible via Pydantic alone."""
    pass


def register_exception_handlers(app) -> None:
    """Register FastAPI exception handlers mapping each exception above to an HTTP status + standard error envelope."""
    pass

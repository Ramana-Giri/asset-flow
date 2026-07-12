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
"""

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.responses import error


class AssetFlowException(Exception):
    """Base class for all domain exceptions in this application."""

    def __init__(self, message: str = "An application error occurred.", *, data=None):
        self.message = message
        self.data = data
        super().__init__(message)


class NotFoundException(AssetFlowException):
    """Raised when a requested entity does not exist."""

    def __init__(self, message: str = "The requested resource was not found.", *, data=None):
        super().__init__(message, data=data)


class PermissionDenied(AssetFlowException):
    """Raised when the current user lacks the required role/permission."""

    def __init__(self, message: str = "You do not have permission to perform this action.", *, data=None):
        super().__init__(message, data=data)


class AssetAlreadyAllocated(AssetFlowException):
    """
    Raised when attempting to allocate an asset that already has an
    Active allocation. Should carry enough context (current holder) for
    the router to surface "currently held by <n>" plus a Transfer
    Request suggestion, per the Allocation screen requirements.
    """

    def __init__(
        self,
        message: str = "This asset is already allocated.",
        *,
        current_holder: str | None = None,
        allocation_id: int | None = None,
        data=None,
    ):
        self.current_holder = current_holder
        self.allocation_id = allocation_id
        payload = data or {}
        if current_holder is not None:
            payload.setdefault("current_holder", current_holder)
        if allocation_id is not None:
            payload.setdefault("allocation_id", allocation_id)
        super().__init__(message, data=payload or None)


class BookingOverlapException(AssetFlowException):
    """Raised when a requested booking time range overlaps an existing Upcoming/Ongoing booking for the same resource."""

    def __init__(self, message: str = "This booking overlaps an existing reservation for this resource.", *, data=None):
        super().__init__(message, data=data)


class TransferNotAllowed(AssetFlowException):
    """Raised when a transfer request is invalid (e.g. no active allocation, invalid target, wrong approver)."""

    def __init__(self, message: str = "This transfer request cannot be processed.", *, data=None):
        super().__init__(message, data=data)


class MaintenanceAlreadyOpen(AssetFlowException):
    """Raised when raising a maintenance request for an asset that already has a non-terminal maintenance request open."""

    def __init__(self, message: str = "This asset already has an open maintenance request.", *, data=None):
        super().__init__(message, data=data)


class DepartmentInactive(AssetFlowException):
    """Raised when an operation targets a Department with status='Inactive' that requires an Active department."""

    def __init__(self, message: str = "This operation requires an active department.", *, data=None):
        super().__init__(message, data=data)


class CircularDepartmentHierarchy(AssetFlowException):
    """Raised when a department update would create a circular parent/child relationship."""

    def __init__(self, message: str = "This change would create a circular department hierarchy.", *, data=None):
        super().__init__(message, data=data)


class ValidationError(AssetFlowException):
    """Raised for cross-field business validation failures not expressible via Pydantic alone."""

    def __init__(self, message: str = "The provided data failed validation.", *, data=None):
        super().__init__(message, data=data)


# Maps each domain exception to the HTTP status code it should translate to.
_EXCEPTION_STATUS_MAP: dict[type[AssetFlowException], int] = {
    NotFoundException: status.HTTP_404_NOT_FOUND,
    PermissionDenied: status.HTTP_403_FORBIDDEN,
    AssetAlreadyAllocated: status.HTTP_409_CONFLICT,
    BookingOverlapException: status.HTTP_409_CONFLICT,
    TransferNotAllowed: status.HTTP_400_BAD_REQUEST,
    MaintenanceAlreadyOpen: status.HTTP_409_CONFLICT,
    DepartmentInactive: status.HTTP_400_BAD_REQUEST,
    CircularDepartmentHierarchy: status.HTTP_400_BAD_REQUEST,
    ValidationError: status.HTTP_422_UNPROCESSABLE_ENTITY,
    # Catch-all for any AssetFlowException raised without a more specific subclass.
    AssetFlowException: status.HTTP_400_BAD_REQUEST,
}


def register_exception_handlers(app: FastAPI) -> None:
    """Register FastAPI exception handlers mapping each exception above to an HTTP status + standard error envelope."""

    def _make_handler(status_code: int):
        async def _handler(request: Request, exc: AssetFlowException) -> JSONResponse:
            envelope = error(message=exc.message,
"""
Standard API Response Envelope

Purpose
-------
Every endpoint returns a consistent {success, message, data} JSON shape.

Responsibilities
-----------------
- Define the envelope model(s) used to wrap every router response.
- Provide success()/error() helper builders.

Interacts With
--------------
- api/v1/*.py -> every router response is wrapped via these helpers.
- core/exceptions.py -> exception handlers build the error envelope via error().
"""

from typing import Any

from pydantic import BaseModel


class APIResponse(BaseModel):
    """Standard response envelope returned by every endpoint."""

    success: bool
    message: str
    data: Any | None = None


def success(data: Any = None, message: str = "OK") -> APIResponse:
    """Build a successful APIResponse envelope."""
    return APIResponse(success=True, message=message, data=data)


def error(message: str, data: Any = None) -> APIResponse:
    """Build an error APIResponse envelope (used by global exception handlers)."""
    return APIResponse(success=False, message=message, data=data)
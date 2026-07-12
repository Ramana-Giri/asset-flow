"""
Allocation Schemas

Purpose
-------
Allocate/Return workflow contracts.

Responsibilities
-----------------
- Validate request payloads (Create/Update/Filter) coming from routers.
- Shape response payloads (Response/List) returned to routers.
- Own field-level VALIDATION rules only (required fields, formats, lengths).
- Never contain business RULES (those belong in the Service layer).

Interacts With
--------------
- api/v1/allocation.py -> routers import these schemas as request/response models.
- services/*.py -> services receive/return these schema objects (not raw ORM models).

NOTE: This file is a structural skeleton only. Method/function bodies are
intentionally left as `pass` (no business logic / SQL / validation code),
per generation scope. Docstrings describe what each piece IS responsible
for once implemented.
"""

from pydantic import BaseModel

# NOTE: In the real implementation, add `from typing import Optional`,
# `from datetime import date, datetime`, ConfigDict(from_attributes=True),
# and Field(...) constraints as needed per class below.


class AllocationCreate(BaseModel):
    """
    asset_id, allocated_to_type (Employee/Department), allocated_to_user_id XOR allocated_to_department_id, expected_return_date (optional).

    Field-level validation constraints (max length, required/optional,
    format) are intentionally omitted from this skeleton and would be
    declared here using Pydantic v2 `Field(...)` / validators.
    """

    pass


class AllocationReturn(BaseModel):
    """
    return_condition_notes for the Return flow.

    Field-level validation constraints (max length, required/optional,
    format) are intentionally omitted from this skeleton and would be
    declared here using Pydantic v2 `Field(...)` / validators.
    """

    pass


class AllocationResponse(BaseModel):
    """
    Allocation representation including overdue flag (derived: status=Active and expected_return_date < today).

    Field-level validation constraints (max length, required/optional,
    format) are intentionally omitted from this skeleton and would be
    declared here using Pydantic v2 `Field(...)` / validators.
    """

    pass


class AllocationListResponse(BaseModel):
    """
    Paginated list wrapper.

    Field-level validation constraints (max length, required/optional,
    format) are intentionally omitted from this skeleton and would be
    declared here using Pydantic v2 `Field(...)` / validators.
    """

    pass


class AllocationFilter(BaseModel):
    """
    Search/filter params: asset_id, user_id, department_id, status, overdue_only.

    Field-level validation constraints (max length, required/optional,
    format) are intentionally omitted from this skeleton and would be
    declared here using Pydantic v2 `Field(...)` / validators.
    """

    pass

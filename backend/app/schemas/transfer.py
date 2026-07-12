"""
Transfer Schemas

Purpose
-------
Transfer request workflow contracts (Requested -> Approved/Rejected -> Completed).

Responsibilities
-----------------
- Validate request payloads (Create/Update/Filter) coming from routers.
- Shape response payloads (Response/List) returned to routers.
- Own field-level VALIDATION rules only (required fields, formats, lengths).
- Never contain business RULES (those belong in the Service layer).

Interacts With
--------------
- api/v1/transfer.py -> routers import these schemas as request/response models.
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


class TransferRequestCreate(BaseModel):
    """
    asset_id, to_user_id XOR to_department_id, reason.

    Field-level validation constraints (max length, required/optional,
    format) are intentionally omitted from this skeleton and would be
    declared here using Pydantic v2 `Field(...)` / validators.
    """

    pass


class TransferDecision(BaseModel):
    """
    Approve/Reject payload used by Asset Manager / Department Head.

    Field-level validation constraints (max length, required/optional,
    format) are intentionally omitted from this skeleton and would be
    declared here using Pydantic v2 `Field(...)` / validators.
    """

    pass


class TransferResponse(BaseModel):
    """
    Transfer representation including resolved asset/target summaries.

    Field-level validation constraints (max length, required/optional,
    format) are intentionally omitted from this skeleton and would be
    declared here using Pydantic v2 `Field(...)` / validators.
    """

    pass


class TransferListResponse(BaseModel):
    """
    Paginated list wrapper.

    Field-level validation constraints (max length, required/optional,
    format) are intentionally omitted from this skeleton and would be
    declared here using Pydantic v2 `Field(...)` / validators.
    """

    pass


class TransferFilter(BaseModel):
    """
    Search/filter params: asset_id, status, requested_by.

    Field-level validation constraints (max length, required/optional,
    format) are intentionally omitted from this skeleton and would be
    declared here using Pydantic v2 `Field(...)` / validators.
    """

    pass

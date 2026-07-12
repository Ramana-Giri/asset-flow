"""
Asset Schemas

Purpose
-------
Asset registration, update, document upload metadata, QR/tag info, filtering/search, and history.

Responsibilities
-----------------
- Validate request payloads (Create/Update/Filter) coming from routers.
- Shape response payloads (Response/List) returned to routers.
- Own field-level VALIDATION rules only (required fields, formats, lengths).
- Never contain business RULES (those belong in the Service layer).

Interacts With
--------------
- api/v1/asset.py -> routers import these schemas as request/response models.
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


class AssetCreate(BaseModel):
    """
    name, category_id, serial_number, acquisition_date/cost, condition, location, department_id, is_bookable, custom_field_values. asset_tag/qr_code are server-generated, never client-supplied.

    Field-level validation constraints (max length, required/optional,
    format) are intentionally omitted from this skeleton and would be
    declared here using Pydantic v2 `Field(...)` / validators.
    """

    pass


class AssetUpdate(BaseModel):
    """
    Editable asset fields (condition, location, department_id, is_bookable, custom_field_values, etc). Status transitions go through dedicated service actions, not a raw field update.

    Field-level validation constraints (max length, required/optional,
    format) are intentionally omitted from this skeleton and would be
    declared here using Pydantic v2 `Field(...)` / validators.
    """

    pass


class AssetDocumentCreate(BaseModel):
    """
    Metadata for an uploaded photo/document (file_type); actual file handled by utils/file_upload.py.

    Field-level validation constraints (max length, required/optional,
    format) are intentionally omitted from this skeleton and would be
    declared here using Pydantic v2 `Field(...)` / validators.
    """

    pass


class AssetDocumentResponse(BaseModel):
    """
    Document representation (file_url, file_type, uploaded_by, uploaded_at).

    Field-level validation constraints (max length, required/optional,
    format) are intentionally omitted from this skeleton and would be
    declared here using Pydantic v2 `Field(...)` / validators.
    """

    pass


class AssetResponse(BaseModel):
    """
    Full asset representation including resolved category/department summaries.

    Field-level validation constraints (max length, required/optional,
    format) are intentionally omitted from this skeleton and would be
    declared here using Pydantic v2 `Field(...)` / validators.
    """

    pass


class AssetListResponse(BaseModel):
    """
    Paginated list wrapper for AssetResponse.

    Field-level validation constraints (max length, required/optional,
    format) are intentionally omitted from this skeleton and would be
    declared here using Pydantic v2 `Field(...)` / validators.
    """

    pass


class AssetFilter(BaseModel):
    """
    Search/filter params: asset_tag, serial_number, qr_code, category_id, status, department_id, location, is_bookable.

    Field-level validation constraints (max length, required/optional,
    format) are intentionally omitted from this skeleton and would be
    declared here using Pydantic v2 `Field(...)` / validators.
    """

    pass


class AssetHistoryResponse(BaseModel):
    """
    Combined allocation history + maintenance history + status history for one asset.

    Field-level validation constraints (max length, required/optional,
    format) are intentionally omitted from this skeleton and would be
    declared here using Pydantic v2 `Field(...)` / validators.
    """

    pass

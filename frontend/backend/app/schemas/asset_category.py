"""
Asset Category Schemas

Purpose
-------
Asset Category CRUD including the JSONB custom_field_schema definition.

Responsibilities
-----------------
- Validate request payloads (Create/Update/Filter) coming from routers.
- Shape response payloads (Response/List) returned to routers.
- Own field-level VALIDATION rules only (required fields, formats, lengths).
- Never contain business RULES (those belong in the Service layer).

Interacts With
--------------
- api/v1/asset_category.py -> routers import these schemas as request/response models.
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


class CustomFieldDefinition(BaseModel):
    """
    Single custom field spec: field name, type, unit/options.

    Field-level validation constraints (max length, required/optional,
    format) are intentionally omitted from this skeleton and would be
    declared here using Pydantic v2 `Field(...)` / validators.
    """

    pass


class AssetCategoryCreate(BaseModel):
    """
    name, description, custom_field_schema (list[CustomFieldDefinition]).

    Field-level validation constraints (max length, required/optional,
    format) are intentionally omitted from this skeleton and would be
    declared here using Pydantic v2 `Field(...)` / validators.
    """

    pass


class AssetCategoryUpdate(BaseModel):
    """
    Editable category fields.

    Field-level validation constraints (max length, required/optional,
    format) are intentionally omitted from this skeleton and would be
    declared here using Pydantic v2 `Field(...)` / validators.
    """

    pass


class AssetCategoryResponse(BaseModel):
    """
    Category representation.

    Field-level validation constraints (max length, required/optional,
    format) are intentionally omitted from this skeleton and would be
    declared here using Pydantic v2 `Field(...)` / validators.
    """

    pass


class AssetCategoryListResponse(BaseModel):
    """
    Paginated list wrapper.

    Field-level validation constraints (max length, required/optional,
    format) are intentionally omitted from this skeleton and would be
    declared here using Pydantic v2 `Field(...)` / validators.
    """

    pass

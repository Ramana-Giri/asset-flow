"""
Report Schemas

Purpose
-------
Reports & Analytics response contracts. All reports return JSON (no PDF generation).

Responsibilities
-----------------
- Validate request payloads (Create/Update/Filter) coming from routers.
- Shape response payloads (Response/List) returned to routers.
- Own field-level VALIDATION rules only (required fields, formats, lengths).
- Never contain business RULES (those belong in the Service layer).

Interacts With
--------------
- api/v1/report.py -> routers import these schemas as request/response models.
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


class AssetUtilizationReport(BaseModel):
    """
    Most-used vs idle assets, utilization trend data points.

    Field-level validation constraints (max length, required/optional,
    format) are intentionally omitted from this skeleton and would be
    declared here using Pydantic v2 `Field(...)` / validators.
    """

    pass


class DepartmentSummaryReport(BaseModel):
    """
    Department-wise allocation summary.

    Field-level validation constraints (max length, required/optional,
    format) are intentionally omitted from this skeleton and would be
    declared here using Pydantic v2 `Field(...)` / validators.
    """

    pass


class MaintenanceSummaryReport(BaseModel):
    """
    Maintenance frequency by asset/category.

    Field-level validation constraints (max length, required/optional,
    format) are intentionally omitted from this skeleton and would be
    declared here using Pydantic v2 `Field(...)` / validators.
    """

    pass


class BookingHeatmapReport(BaseModel):
    """
    Resource booking heatmap (peak usage windows).

    Field-level validation constraints (max length, required/optional,
    format) are intentionally omitted from this skeleton and would be
    declared here using Pydantic v2 `Field(...)` / validators.
    """

    pass


class IdleAssetsReport(BaseModel):
    """
    Assets nearing retirement / due for maintenance / unused for N days.

    Field-level validation constraints (max length, required/optional,
    format) are intentionally omitted from this skeleton and would be
    declared here using Pydantic v2 `Field(...)` / validators.
    """

    pass

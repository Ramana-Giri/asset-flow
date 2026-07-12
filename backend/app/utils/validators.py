"""
Reusable Validation Functions

Purpose
-------
Cross-field / cross-entity validation helpers reused by multiple schemas or services (beyond simple Pydantic field validation).

Responsibilities
-----------------
- validate_custom_field_values(schema, values): check an asset's custom_field_values against its category's custom_field_schema.
- validate_date_range(start, end): generic start<=end check (audits, etc).

Interacts With
--------------
- services/asset_service.py, services/audit_service.py -> call these during create/update flows.

NOTE: This file is a structural skeleton only. Method/function bodies are
intentionally left as `pass` (no business logic / SQL / validation code),
per generation scope. Docstrings describe what each piece IS responsible
for once implemented.
"""

def validate_custom_field_values(schema: list, values: dict) -> None:
    """Validate that `values` conforms to the category's custom_field_schema (types/required fields)."""
    pass


def validate_date_range(start_date, end_date) -> None:
    """Validate that end_date is not before start_date; raise ValidationError otherwise."""
    pass

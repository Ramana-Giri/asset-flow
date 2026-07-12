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
"""

from datetime import date, datetime
from typing import Any, Dict, List, Optional, Union

from app.core.exceptions import ValidationError

# Maps custom_field_schema "type" strings to acceptable Python types.
_TYPE_MAP = {
    "string": str,
    "text": str,
    "number": (int, float),
    "boolean": bool,
    "date": (str, date, datetime),  # dates typically arrive as ISO strings over JSON
}


def validate_custom_field_values(schema: List[Dict[str, Any]], values: Dict[str, Any]) -> None:
    """Validate that `values` conforms to the category's custom_field_schema (types/required fields).

    `schema` entries look like: {"field": "warranty_period", "type": "number",
    "unit": "months", "required": true}. Unknown keys in `values` that
    aren't declared in `schema` are rejected to catch typos/garbage input.
    """
    schema = schema or []
    values = values or {}

    declared_fields = {entry["field"] for entry in schema if "field" in entry}
    unknown_fields = set(values.keys()) - declared_fields
    if unknown_fields:
        raise ValidationError(
            f"Unknown custom field(s) not defined on this category: {', '.join(sorted(unknown_fields))}"
        )

    for entry in schema:
        field_name = entry.get("field")
        if field_name is None:
            continue

        field_type = entry.get("type", "string")
        is_required = entry.get("required", False)
        has_value = field_name in values and values[field_name] is not None

        if is_required and not has_value:
            raise ValidationError(f"Custom field '{field_name}' is required.")

        if not has_value:
            continue

        expected_python_type = _TYPE_MAP.get(field_type)
        if expected_python_type and not isinstance(values[field_name], expected_python_type):
            raise ValidationError(
                f"Custom field '{field_name}' expected type '{field_type}', "
                f"got '{type(values[field_name]).__name__}'."
            )


def validate_date_range(start_date: Optional[Union[date, datetime]], end_date: Optional[Union[date, datetime]]) -> None:
    """Validate that end_date is not before start_date; raise ValidationError otherwise."""
    if start_date is None or end_date is None:
        return
    if end_date < start_date:
        raise ValidationError("End date cannot be before start date.")
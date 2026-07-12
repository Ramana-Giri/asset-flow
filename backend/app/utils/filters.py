"""
Dynamic Filtering Helper

Purpose
-------
Reusable helper to apply a dict of filter params onto a SQLAlchemy select() statement.

Responsibilities
-----------------
- apply_filters(query, model, filters): translate a filter dict (e.g. AssetFilter.model_dump(exclude_none=True)) into WHERE clauses.

Interacts With
--------------
- repositories/*.py -> search() methods use this alongside pagination.py.
- schemas/*.py -> *Filter schemas define the shape passed in here.
"""

from typing import Any, Dict

from sqlalchemy.sql import Select

# Suffixes recognised on filter dict keys, translated into comparison operators.
# e.g. {"acquisition_cost__gte": 100} -> Model.acquisition_cost >= 100
_SUFFIX_OPS = {
    "__gte": lambda col, val: col >= val,
    "__lte": lambda col, val: col <= val,
    "__gt": lambda col, val: col > val,
    "__lt": lambda col, val: col < val,
    "__ne": lambda col, val: col != val,
    "__like": lambda col, val: col.ilike(f"%{val}%"),
    "__in": lambda col, val: col.in_(val),
}


def apply_filters(query: Select, model: type, filters: Dict[str, Any]) -> Select:
    """Apply each non-None key in `filters` as an equality/range WHERE clause on `model`.

    Plain keys (e.g. "status") become equality filters. Keys with a
    recognised suffix (e.g. "acquisition_cost__gte") become range/text/
    membership filters. Keys that don't map to a column on `model`, or
    whose value is None, are skipped silently.
    """
    if not filters:
        return query

    for key, value in filters.items():
        if value is None:
            continue

        matched_suffix = next((suffix for suffix in _SUFFIX_OPS if key.endswith(suffix)), None)
        if matched_suffix:
            field_name = key[: -len(matched_suffix)]
            op = _SUFFIX_OPS[matched_suffix]
        else:
            field_name = key
            op = lambda col, val: col == val

        column = getattr(model, field_name, None)
        if column is None:
            continue

        query = query.where(op(column, value))

    return query
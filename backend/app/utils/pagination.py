"""
Pagination Helper

Purpose
-------
Reusable pagination logic shared by every repository's list/search methods.

Responsibilities
-----------------
- paginate(query, skip, limit): apply OFFSET/LIMIT and return (items, total_count).
- Define a generic PageResult container.

Interacts With
--------------
- repositories/base.py -> list_all()/search() use this.
- schemas/*.py -> *ListResponse schemas mirror this shape (items, total, skip, limit).

NOTE: This file is a structural skeleton only. Method/function bodies are
intentionally left as `pass` (no business logic / SQL / validation code),
per generation scope. Docstrings describe what each piece IS responsible
for once implemented.
"""

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class PageResult(Generic[T]):
    """Generic paginated result container."""
    items: list
    total: int
    skip: int
    limit: int


async def paginate(query, skip: int, limit: int) -> PageResult:
    """Apply OFFSET/LIMIT to a SQLAlchemy select() and return items + total count."""
    pass

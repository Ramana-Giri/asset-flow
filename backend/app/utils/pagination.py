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
"""

from dataclasses import dataclass, field
from typing import Generic, List, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from app.core.constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

T = TypeVar("T")


@dataclass
class PageResult(Generic[T]):
    """Generic paginated result container."""
    items: List[T] = field(default_factory=list)
    total: int = 0
    skip: int = 0
    limit: int = DEFAULT_PAGE_SIZE


async def paginate(
    session: AsyncSession,
    query: Select,
    skip: int = 0,
    limit: int = DEFAULT_PAGE_SIZE,
) -> PageResult:
    """Apply OFFSET/LIMIT to a SQLAlchemy select() and return items + total count.

    `query` should be an unpaginated select() statement. Runs a COUNT(*)
    over the same filtered subquery to get `total`, then re-runs the
    original query with OFFSET/LIMIT applied for `items`.

    NOTE: requires an active AsyncSession to execute against (added beyond
    the checklist's bare `paginate(query, skip, limit)` signature, since
    running a query async requires a session to execute it on).
    """
    skip = max(skip, 0)
    limit = min(max(limit, 1), MAX_PAGE_SIZE)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await session.execute(count_query)).scalar_one()

    paged_query = query.offset(skip).limit(limit)
    result = await session.execute(paged_query)
    items = list(result.scalars().all())

    return PageResult(items=items, total=total, skip=skip, limit=limit)
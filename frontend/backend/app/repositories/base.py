"""
Base Repository

Purpose
-------
Generic reusable CRUD/query scaffolding shared by every concrete repository, so entity repositories only declare entity-specific finder methods.

Responsibilities
-----------------
- Provide generic find_by_id / create / update / delete / list methods over a given ORM model.
- Provide generic pagination support (see utils/pagination.py) and dynamic filtering support (see utils/filters.py).
- Accept an AsyncSession via constructor injection (see dependencies.py -> get_db()).
- Contain ONLY database operations - no business rules, no HTTP exceptions.

Interacts With
--------------
- db/database.py -> receives an AsyncSession created there.
- Concrete repositories (e.g. AssetRepository) subclass this for shared CRUD behaviour.
- utils/pagination.py, utils/filters.py -> reused here for list/search operations.

NOTE: This file is a structural skeleton only. Method/function bodies are
intentionally left as `pass` (no business logic / SQL / validation code),
per generation scope. Docstrings describe what each piece IS responsible
for once implemented.
"""

from typing import Generic, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """
    Generic repository providing common CRUD operations for a single
    SQLAlchemy model. Concrete repositories subclass this and add
    entity-specific query methods.
    """

    def __init__(self, session: AsyncSession, model: type[ModelType]):
        """Store the active DB session and the ORM model this repository manages."""
        self.session = session
        self.model = model

    async def find_by_id(self, id_: int):
        """Fetch a single row by primary key, or None if not found."""
        pass

    async def list_all(self, skip: int = 0, limit: int = 50):
        """Fetch a page of rows (see utils/pagination.py for the shared page contract)."""
        pass

    async def create(self, data: dict):
        """Insert a new row from a validated dict (typically schema.model_dump())."""
        pass

    async def update(self, id_: int, data: dict):
        """Patch an existing row by primary key with the given field values."""
        pass

    async def delete(self, id_: int):
        """Hard-delete or soft-deactivate a row, depending on entity semantics."""
        pass

    async def search(self, filters: dict, skip: int = 0, limit: int = 50):
        """Apply dynamic filters (see utils/filters.py) and return a paginated result."""
        pass

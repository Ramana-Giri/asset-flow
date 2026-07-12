"""
Declarative Base

Purpose
-------
Single shared SQLAlchemy DeclarativeBase every model inherits from.

Responsibilities
-----------------
- Declare `class Base(DeclarativeBase): pass`.

Interacts With
--------------
- db/models/*.py -> every model inherits Base.
- alembic/env.py -> imports Base.metadata for autogenerate.

NOTE: This file is a structural skeleton only. Method/function bodies are
intentionally left as `pass` (no business logic / SQL / validation code),
per generation scope. Docstrings describe what each piece IS responsible
for once implemented.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Shared declarative base class for every ORM model in db/models/."""
    pass

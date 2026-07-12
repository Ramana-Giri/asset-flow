"""
Alembic Migration Environment

Purpose
-------
Wires Alembic's autogenerate/migration runner to this project's SQLAlchemy Base and DATABASE_URL.

Responsibilities
-----------------
- Import app.db.base.Base and app.db.models (so every model is registered on Base.metadata).
- Set target_metadata = Base.metadata for autogenerate.
- Read the DB URL from app.config.settings instead of a hardcoded value.

Interacts With
--------------
- db/base.py, db/models/__init__.py -> supply target_metadata.
- config.py -> DATABASE_URL.

NOTE: This file is a structural skeleton only. Method/function bodies are
intentionally left as `pass` (no business logic / SQL / validation code),
per generation scope. Docstrings describe what each piece IS responsible
for once implemented.
"""

from alembic import context

# from app.db.base import Base
# from app.db import models  # noqa: F401  (ensures all models are registered)
# from app.config import settings

# target_metadata = Base.metadata

# NOTE: This is the standard schema.sql-first project: assetflow_schema.sql
# is the authoritative source of truth (already includes ENUM types, the
# booking EXCLUDE constraint, the asset_tag trigger, etc). Alembic is
# wired here primarily for incremental changes going forward; the initial
# migration should be generated with --autogenerate against a DB already
# created from assetflow_schema.sql, then reviewed for parity.


def run_migrations_offline():
    """Run migrations in 'offline' mode (no live DB connection)."""
    pass


def run_migrations_online():
    """Run migrations in 'online' mode (with a live DB connection)."""
    pass


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

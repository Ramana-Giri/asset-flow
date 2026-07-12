"""
ActivityLog Model  (table: "activity_logs")

Purpose
-------
Immutable audit trail entry: who did what, to which entity, when.

Responsibilities
-----------------
- Maps ORM attributes 1:1 to the "activity_logs" table defined in assetflow_schema.sql.
- Declares relationships to related entities for ORM (lazy) navigation.
- Contains NO business logic, NO validation logic, NO query logic.

Interacts With
--------------
- db/base.py -> inherits the shared DeclarativeBase.
- repositories/*_repository.py -> the only layer permitted to query/persist ActivityLog directly.
- SQLAlchemy relationship()s mirror the FKs declared in assetflow_schema.sql.

NOTE: This file is a structural skeleton only. Method/function bodies are
intentionally left as `pass` (no business logic / SQL / validation code),
per generation scope. Docstrings describe what each piece IS responsible
for once implemented.
"""

from app.db.base import Base

# Column and relationship declarations are intentionally omitted from this
# skeleton (SQLAlchemy 2.0 `Mapped` / `mapped_column` / `relationship`
# constructs would go here). The authoritative column list, types,
# constraints and indexes for this table live in assetflow_schema.sql.


class ActivityLog(Base):
    """
    ORM model for the "activity_logs" table.

    Columns (see assetflow_schema.sql for authoritative types/constraints):
    # - id: SERIAL PK
    # - user_id: FK -> users.id (nullable, SET NULL on user delete)
    # - action: VARCHAR(100) NOT NULL (e.g. CREATE_ASSET, APPROVE_MAINTENANCE)
    # - entity_type: VARCHAR(50) NOT NULL
    # - entity_id: INT (nullable)
    # - details: JSONB (nullable)
    # - ip_address: VARCHAR(64)
    # - created_at: TIMESTAMPTZ

    Relationships:
    # - user: User (many-to-one, nullable)
    """

    __tablename__ = "activity_logs"

    # TODO (structure only, not implemented here): declare mapped_column()
    # attributes and relationship() attributes matching the lists above.
    pass

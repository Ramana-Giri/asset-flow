"""
AssetStatusHistory Model  (table: "asset_status_history")

Purpose
-------
Full lifecycle audit trail of every asset status transition (Available <-> Under Maintenance, etc). Populated automatically by a DB trigger (log_asset_status_change) whenever assets.status changes, in addition to any explicit service-side inserts.

Responsibilities
-----------------
- Maps ORM attributes 1:1 to the "asset_status_history" table defined in assetflow_schema.sql.
- Declares relationships to related entities for ORM (lazy) navigation.
- Contains NO business logic, NO validation logic, NO query logic.

Interacts With
--------------
- db/base.py -> inherits the shared DeclarativeBase.
- repositories/*_repository.py -> the only layer permitted to query/persist AssetStatusHistory directly.
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


class AssetStatusHistory(Base):
    """
    ORM model for the "asset_status_history" table.

    Columns (see assetflow_schema.sql for authoritative types/constraints):
    # - id: SERIAL PK
    # - asset_id: FK -> assets.id NOT NULL
    # - old_status / new_status: asset_status ENUM (old nullable)
    # - changed_by: FK -> users.id (nullable)
    # - reason: VARCHAR(255)
    # - reference_type: VARCHAR(50) (Allocation, Maintenance, Audit, Manual)
    # - reference_id: INT (nullable)
    # - changed_at: TIMESTAMPTZ

    Relationships:
    # - asset: Asset (many-to-one)
    # - changed_by_user: User (many-to-one, nullable)
    """

    __tablename__ = "asset_status_history"

    # TODO (structure only, not implemented here): declare mapped_column()
    # attributes and relationship() attributes matching the lists above.
    pass

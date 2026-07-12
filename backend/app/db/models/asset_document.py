"""
AssetDocument Model  (table: "asset_documents")

Purpose
-------
A photo/document (invoice, manual, image) attached to an asset.

Responsibilities
-----------------
- Maps ORM attributes 1:1 to the "asset_documents" table defined in assetflow_schema.sql.
- Declares relationships to related entities for ORM (lazy) navigation.
- Contains NO business logic, NO validation logic, NO query logic.

Interacts With
--------------
- db/base.py -> inherits the shared DeclarativeBase.
- repositories/*_repository.py -> the only layer permitted to query/persist AssetDocument directly.
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


class AssetDocument(Base):
    """
    ORM model for the "asset_documents" table.

    Columns (see assetflow_schema.sql for authoritative types/constraints):
    # - id: SERIAL PK
    # - asset_id: FK -> assets.id NOT NULL
    # - file_url: VARCHAR(500) NOT NULL
    # - file_type: VARCHAR(50) (Photo, Invoice, Manual, etc.)
    # - uploaded_by: FK -> users.id (nullable)
    # - uploaded_at: TIMESTAMPTZ

    Relationships:
    # - asset: Asset (many-to-one)
    # - uploaded_by_user: User (many-to-one, nullable)
    """

    __tablename__ = "asset_documents"

    # TODO (structure only, not implemented here): declare mapped_column()
    # attributes and relationship() attributes matching the lists above.
    pass

"""
AssetCategory Model  (table: "asset_categories")

Purpose
-------
Category taxonomy for assets (Electronics, Furniture, Vehicles, ...) with a JSONB custom-field schema for category-specific optional fields (e.g. warranty_period).

Responsibilities
-----------------
- Maps ORM attributes 1:1 to the "asset_categories" table defined in assetflow_schema.sql.
- Declares relationships to related entities for ORM (lazy) navigation.
- Contains NO business logic, NO validation logic, NO query logic.

Interacts With
--------------
- db/base.py -> inherits the shared DeclarativeBase.
- repositories/*_repository.py -> the only layer permitted to query/persist AssetCategory directly.
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


class AssetCategory(Base):
    """
    ORM model for the "asset_categories" table.

    Columns (see assetflow_schema.sql for authoritative types/constraints):
    # - id: SERIAL PK
    # - name: VARCHAR(100) UNIQUE NOT NULL
    # - description: TEXT
    # - custom_field_schema: JSONB (list of {field, type, unit} definitions)
    # - created_at / updated_at: TIMESTAMPTZ

    Relationships:
    # - assets: list[Asset] (assets registered under this category)
    """

    __tablename__ = "asset_categories"

    # TODO (structure only, not implemented here): declare mapped_column()
    # attributes and relationship() attributes matching the lists above.
    pass

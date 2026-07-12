"""
Asset Model  (table: "assets")

Purpose
-------
Central asset record: identity, lifecycle status, ownership, and bookable flag. Asset Tag is auto-generated (AF-0001...) by a DB trigger/sequence.

Responsibilities
-----------------
- Maps ORM attributes 1:1 to the "assets" table defined in assetflow_schema.sql.
- Declares relationships to related entities for ORM (lazy) navigation.
- Contains NO business logic, NO validation logic, NO query logic.

Interacts With
--------------
- db/base.py -> inherits the shared DeclarativeBase.
- repositories/*_repository.py -> the only layer permitted to query/persist Asset directly.
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


class Asset(Base):
    """
    ORM model for the "assets" table.

    Columns (see assetflow_schema.sql for authoritative types/constraints):
    # - id: SERIAL PK
    # - asset_tag: VARCHAR(20) UNIQUE (auto-generated, e.g. AF-0001)
    # - name: VARCHAR(150) NOT NULL
    # - category_id: FK -> asset_categories.id NOT NULL
    # - serial_number: VARCHAR(100) UNIQUE
    # - acquisition_date: DATE
    # - acquisition_cost: NUMERIC(12,2) (reporting/ranking only, NOT linked to accounting)
    # - condition: asset_condition ENUM ('Excellent','Good','Fair','Poor','Damaged')
    # - location: VARCHAR(150)
    # - department_id: FK -> departments.id (nullable, owning department)
    # - status: asset_status ENUM ('Available','Allocated','Reserved','Under Maintenance','Lost','Retired','Disposed')
    # - is_bookable: BOOLEAN (shared/bookable flag)
    # - qr_code: VARCHAR(150) UNIQUE
    # - custom_field_values: JSONB (values matching the category's custom_field_schema)
    # - created_by: FK -> users.id
    # - created_at / updated_at: TIMESTAMPTZ

    Relationships:
    # - category: AssetCategory (many-to-one)
    # - department: Department (many-to-one)
    # - created_by_user: User (many-to-one)
    # - documents: list[AssetDocument]
    # - status_history: list[AssetStatusHistory]
    # - allocations: list[Allocation]
    # - transfer_requests: list[TransferRequest]
    # - bookings: list[ResourceBooking]
    # - maintenance_requests: list[MaintenanceRequest]
    # - audit_items: list[AuditItem]
    """

    __tablename__ = "assets"

    # TODO (structure only, not implemented here): declare mapped_column()
    # attributes and relationship() attributes matching the lists above.
    pass

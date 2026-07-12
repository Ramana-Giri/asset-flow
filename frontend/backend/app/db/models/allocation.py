"""
Allocation Model  (table: "allocations")

Purpose
-------
Records an asset being held by an employee OR a department. A DB partial unique index guarantees only one 'Active' allocation per asset at a time (no double-allocation).

Responsibilities
-----------------
- Maps ORM attributes 1:1 to the "allocations" table defined in assetflow_schema.sql.
- Declares relationships to related entities for ORM (lazy) navigation.
- Contains NO business logic, NO validation logic, NO query logic.

Interacts With
--------------
- db/base.py -> inherits the shared DeclarativeBase.
- repositories/*_repository.py -> the only layer permitted to query/persist Allocation directly.
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


class Allocation(Base):
    """
    ORM model for the "allocations" table.

    Columns (see assetflow_schema.sql for authoritative types/constraints):
    # - id: SERIAL PK
    # - asset_id: FK -> assets.id NOT NULL
    # - allocated_to_type: allocation_target ENUM ('Employee','Department')
    # - allocated_to_user_id: FK -> users.id (nullable, set when target=Employee)
    # - allocated_to_department_id: FK -> departments.id (nullable, set when target=Department)
    # - allocated_by: FK -> users.id NOT NULL (Asset Manager)
    # - allocation_date: DATE DEFAULT CURRENT_DATE
    # - expected_return_date: DATE (nullable)
    # - actual_return_date: DATE (nullable)
    # - return_condition_notes: TEXT
    # - returned_by: FK -> users.id (nullable)
    # - status: allocation_status ENUM ('Active','Returned')
    # - created_at / updated_at: TIMESTAMPTZ
    # - CHECK chk_allocation_target: exactly one of user/department set based on allocated_to_type
    # - UNIQUE INDEX uq_one_active_allocation_per_asset: WHERE status='Active'

    Relationships:
    # - asset: Asset (many-to-one)
    # - allocated_to_user: User (many-to-one, nullable)
    # - allocated_to_department: Department (many-to-one, nullable)
    # - allocated_by_user: User (many-to-one, Asset Manager)
    # - returned_by_user: User (many-to-one, nullable)
    # - transfer_requests_from: list[TransferRequest] (as from_allocation)
    """

    __tablename__ = "allocations"

    # TODO (structure only, not implemented here): declare mapped_column()
    # attributes and relationship() attributes matching the lists above.
    pass

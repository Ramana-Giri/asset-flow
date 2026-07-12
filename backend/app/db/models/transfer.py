"""
TransferRequest Model  (table: "transfer_requests")

Purpose
-------
Requested -> Approved/Rejected -> Completed workflow for moving an already-allocated asset to a new holder.

Responsibilities
-----------------
- Maps ORM attributes 1:1 to the "transfer_requests" table defined in assetflow_schema.sql.
- Declares relationships to related entities for ORM (lazy) navigation.
- Contains NO business logic, NO validation logic, NO query logic.

Interacts With
--------------
- db/base.py -> inherits the shared DeclarativeBase.
- repositories/*_repository.py -> the only layer permitted to query/persist TransferRequest directly.
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


class TransferRequest(Base):
    """
    ORM model for the "transfer_requests" table.

    Columns (see assetflow_schema.sql for authoritative types/constraints):
    # - id: SERIAL PK
    # - asset_id: FK -> assets.id NOT NULL
    # - from_allocation_id: FK -> allocations.id (nullable)
    # - requested_by: FK -> users.id NOT NULL
    # - to_user_id: FK -> users.id (nullable)
    # - to_department_id: FK -> departments.id (nullable)
    # - reason: TEXT
    # - status: transfer_status ENUM ('Requested','Approved','Rejected','Completed')
    # - approved_by: FK -> users.id (nullable, Asset Manager / Department Head)
    # - approved_at: TIMESTAMPTZ (nullable)
    # - new_allocation_id: FK -> allocations.id (nullable, set once re-allocated)
    # - created_at / updated_at: TIMESTAMPTZ
    # - CHECK chk_transfer_target: to_user_id IS NOT NULL OR to_department_id IS NOT NULL

    Relationships:
    # - asset: Asset (many-to-one)
    # - from_allocation: Allocation (many-to-one, nullable)
    # - new_allocation: Allocation (many-to-one, nullable)
    # - requested_by_user: User (many-to-one)
    # - approved_by_user: User (many-to-one, nullable)
    # - to_user: User (many-to-one, nullable)
    # - to_department: Department (many-to-one, nullable)
    """

    __tablename__ = "transfer_requests"

    # TODO (structure only, not implemented here): declare mapped_column()
    # attributes and relationship() attributes matching the lists above.
    pass

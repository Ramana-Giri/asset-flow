"""
User Model  (table: "users")

Purpose
-------
Employee directory + authentication identity. Signup always creates role=Employee; only Admin promotes to Department Head / Asset Manager.

Responsibilities
-----------------
- Maps ORM attributes 1:1 to the "users" table defined in assetflow_schema.sql.
- Declares relationships to related entities for ORM (lazy) navigation.
- Contains NO business logic, NO validation logic, NO query logic.

Interacts With
--------------
- db/base.py -> inherits the shared DeclarativeBase.
- repositories/*_repository.py -> the only layer permitted to query/persist User directly.
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


class User(Base):
    """
    ORM model for the "users" table.

    Columns (see assetflow_schema.sql for authoritative types/constraints):
    # - id: SERIAL PK
    # - name: VARCHAR(150) NOT NULL
    # - email: VARCHAR(150) UNIQUE NOT NULL
    # - password_hash: VARCHAR(255) NOT NULL (bcrypt)
    # - role: user_role ENUM ('Admin','Asset Manager','Department Head','Employee')
    # - department_id: FK -> departments.id (nullable)
    # - status: account_status ENUM ('Active','Inactive')
    # - promoted_by: FK -> users.id (nullable, Admin who promoted this user)
    # - promoted_at: TIMESTAMPTZ (nullable)
    # - created_at / updated_at: TIMESTAMPTZ

    Relationships:
    # - department: Department (many-to-one)
    # - promoted_by_user: User (self-referential)
    # - sessions: list[UserSession]
    # - password_reset_tokens: list[PasswordResetToken]
    # - allocations_received: list[Allocation] (as allocated_to_user)
    # - allocations_made: list[Allocation] (as allocated_by, Asset Manager)
    # - maintenance_requests_raised: list[MaintenanceRequest]
    # - bookings: list[ResourceBooking]
    # - notifications: list[Notification]
    # - activity_logs: list[ActivityLog]
    """

    __tablename__ = "users"

    # TODO (structure only, not implemented here): declare mapped_column()
    # attributes and relationship() attributes matching the lists above.
    pass

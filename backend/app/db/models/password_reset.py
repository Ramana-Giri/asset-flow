"""
PasswordResetToken Model  (table: "password_reset_tokens")

Purpose
-------
Single-use, expiring token issued for the Forgot Password / Reset Password flow.

Responsibilities
-----------------
- Maps ORM attributes 1:1 to the "password_reset_tokens" table defined in assetflow_schema.sql.
- Declares relationships to related entities for ORM (lazy) navigation.
- Contains NO business logic, NO validation logic, NO query logic.

Interacts With
--------------
- db/base.py -> inherits the shared DeclarativeBase.
- repositories/*_repository.py -> the only layer permitted to query/persist PasswordResetToken directly.
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


class PasswordResetToken(Base):
    """
    ORM model for the "password_reset_tokens" table.

    Columns (see assetflow_schema.sql for authoritative types/constraints):
    # - id: SERIAL PK
    # - user_id: FK -> users.id NOT NULL
    # - token: VARCHAR(255) UNIQUE NOT NULL
    # - expires_at: TIMESTAMPTZ NOT NULL
    # - used: BOOLEAN DEFAULT FALSE
    # - created_at: TIMESTAMPTZ

    Relationships:
    # - user: User (many-to-one)
    """

    __tablename__ = "password_reset_tokens"

    # TODO (structure only, not implemented here): declare mapped_column()
    # attributes and relationship() attributes matching the lists above.
    pass

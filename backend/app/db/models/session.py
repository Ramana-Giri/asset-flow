"""
UserSession Model  (table: "user_sessions")

Purpose
-------
Server-side session record used for login/logout and Session Validation. Auth is session-token based (NOT JWT): an opaque, random, non-guessable token is generated at login, stored here with an expiry, and validated on each request.

Responsibilities
-----------------
- Maps ORM attributes 1:1 to the "user_sessions" table defined in assetflow_schema.sql.
- Declares relationships to related entities for ORM (lazy) navigation.
- Contains NO business logic, NO validation logic, NO query logic.

Interacts With
--------------
- db/base.py -> inherits the shared DeclarativeBase.
- repositories/*_repository.py -> the only layer permitted to query/persist UserSession directly.
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


class UserSession(Base):
    """
    ORM model for the "user_sessions" table.

    Columns (see assetflow_schema.sql for authoritative types/constraints):
    # - id: SERIAL PK
    # - user_id: FK -> users.id NOT NULL
    # - session_token: VARCHAR(255) UNIQUE NOT NULL (opaque random token, NOT a JWT)
    # - ip_address: VARCHAR(64)
    # - user_agent: TEXT
    # - expires_at: TIMESTAMPTZ NOT NULL
    # - created_at / last_active_at: TIMESTAMPTZ

    Relationships:
    # - user: User (many-to-one)
    """

    __tablename__ = "user_sessions"

    # TODO (structure only, not implemented here): declare mapped_column()
    # attributes and relationship() attributes matching the lists above.
    pass

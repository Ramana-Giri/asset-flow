"""
ResourceBooking Model  (table: "resource_bookings")

Purpose
-------
Time-slot booking of a shared/bookable asset. Overlap prevention is enforced at the DB level via a GiST EXCLUDE constraint on (asset_id, time-range) for Upcoming/Ongoing bookings, in addition to any service-layer pre-check.

Responsibilities
-----------------
- Maps ORM attributes 1:1 to the "resource_bookings" table defined in assetflow_schema.sql.
- Declares relationships to related entities for ORM (lazy) navigation.
- Contains NO business logic, NO validation logic, NO query logic.

Interacts With
--------------
- db/base.py -> inherits the shared DeclarativeBase.
- repositories/*_repository.py -> the only layer permitted to query/persist ResourceBooking directly.
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


class ResourceBooking(Base):
    """
    ORM model for the "resource_bookings" table.

    Columns (see assetflow_schema.sql for authoritative types/constraints):
    # - id: SERIAL PK
    # - asset_id: FK -> assets.id NOT NULL
    # - booked_by: FK -> users.id NOT NULL
    # - department_id: FK -> departments.id (nullable, booked on behalf of)
    # - start_time / end_time: TIMESTAMPTZ NOT NULL
    # - purpose: VARCHAR(255)
    # - status: booking_status ENUM ('Upcoming','Ongoing','Completed','Cancelled')
    # - cancelled_by: FK -> users.id (nullable)
    # - cancelled_at: TIMESTAMPTZ (nullable)
    # - created_at / updated_at: TIMESTAMPTZ
    # - CHECK chk_booking_time: end_time > start_time
    # - EXCLUDE excl_no_overlapping_bookings: GiST (asset_id =, tstzrange(start_time,end_time,'[)') &&) WHERE status IN ('Upcoming','Ongoing')

    Relationships:
    # - asset: Asset (many-to-one)
    # - booked_by_user: User (many-to-one)
    # - department: Department (many-to-one, nullable)
    # - cancelled_by_user: User (many-to-one, nullable)
    """

    __tablename__ = "resource_bookings"

    # TODO (structure only, not implemented here): declare mapped_column()
    # attributes and relationship() attributes matching the lists above.
    pass

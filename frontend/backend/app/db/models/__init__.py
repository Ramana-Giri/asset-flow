"""
Models Package Init

Purpose
-------
Aggregates every ORM model so Alembic autogenerate and Base.metadata can discover all mapped tables from a single import.

Responsibilities
-----------------
- Re-export every model class defined under db/models/.
- Ensure all models are registered on Base.metadata before Alembic 'autogenerate' or 'create_all' runs.

Interacts With
--------------
- db/base.py -> the shared Base these models attach their metadata to.
- alembic/env.py -> imports this package to discover all models.

NOTE: This file is a structural skeleton only. Method/function bodies are
intentionally left as `pass` (no business logic / SQL / validation code),
per generation scope. Docstrings describe what each piece IS responsible
for once implemented.
"""

from app.db.models.department import Department  # noqa: F401
from app.db.models.asset_category import AssetCategory  # noqa: F401
from app.db.models.user import User  # noqa: F401
from app.db.models.password_reset import PasswordResetToken  # noqa: F401
from app.db.models.session import UserSession  # noqa: F401
from app.db.models.asset import Asset  # noqa: F401
from app.db.models.allocation import Allocation  # noqa: F401
from app.db.models.transfer import TransferRequest  # noqa: F401
from app.db.models.booking import ResourceBooking  # noqa: F401
from app.db.models.maintenance import MaintenanceRequest  # noqa: F401
from app.db.models.notification import Notification  # noqa: F401
from app.db.models.activity_log import ActivityLog  # noqa: F401
from app.db.models.audit_cycle import AuditCycle  # noqa: F401
from app.db.models.audit_cycle_auditor import AuditCycleAuditor  # noqa: F401
from app.db.models.audit_item import AuditItem  # noqa: F401
from app.db.models.asset_document import AssetDocument  # noqa: F401
from app.db.models.asset_status_history import AssetStatusHistory  # noqa: F401

"""
Top-Level API Router

Purpose
-------
Aggregates every v1 module router under a single APIRouter mounted in main.py.

Responsibilities
-----------------
- Import every module router from api/v1/.
- include_router() each one onto a shared prefix (e.g. /api/v1).

Interacts With
--------------
- main.py -> includes this aggregate router on the FastAPI app.
- api/v1/*.py -> the individual module routers being aggregated.

NOTE: This file is a structural skeleton only. Method/function bodies are
intentionally left as `pass` (no business logic / SQL / validation code),
per generation scope. Docstrings describe what each piece IS responsible
for once implemented.
"""

from fastapi import APIRouter

from app.api.v1 import auth
from app.api.v1 import users
from app.api.v1 import departments
from app.api.v1 import asset_categories
from app.api.v1 import assets
from app.api.v1 import allocations
from app.api.v1 import transfers
from app.api.v1 import bookings
from app.api.v1 import maintenance
from app.api.v1 import audits
from app.api.v1 import notifications
from app.api.v1 import activity_logs
from app.api.v1 import dashboard
from app.api.v1 import reports

api_router = APIRouter()

# Each module router is mounted here with its own prefix/tag (declared in
# the module itself). Left commented in this skeleton:
# api_router.include_router(auth.router)
# api_router.include_router(users.router)
# api_router.include_router(departments.router)
# api_router.include_router(asset_categories.router)
# api_router.include_router(assets.router)
# api_router.include_router(allocations.router)
# api_router.include_router(transfers.router)
# api_router.include_router(bookings.router)
# api_router.include_router(maintenance.router)
# api_router.include_router(audits.router)
# api_router.include_router(notifications.router)
# api_router.include_router(activity_logs.router)
# api_router.include_router(dashboard.router)
# api_router.include_router(reports.router)

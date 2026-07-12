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

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(departments.router)
api_router.include_router(asset_categories.router)
api_router.include_router(assets.router)
api_router.include_router(allocations.router)
api_router.include_router(transfers.router)
api_router.include_router(bookings.router)
api_router.include_router(maintenance.router)
api_router.include_router(audits.router)
api_router.include_router(notifications.router)
api_router.include_router(activity_logs.router)
api_router.include_router(dashboard.router)
api_router.include_router(reports.router)
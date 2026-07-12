from __future__ import annotations

from app.repositories.asset_repository import AssetRepository
from app.repositories.allocation_repository import AllocationRepository
from app.repositories.maintenance_repository import MaintenanceRepository
from app.repositories.booking_repository import BookingRepository
from app.repositories.transfer_repository import TransferRepository
from app.repositories.activity_log_repository import ActivityLogRepository


class DashboardService:
    def __init__(
        self,
        asset_repository: AssetRepository,
        allocation_repository: AllocationRepository,
        maintenance_repository: MaintenanceRepository,
        booking_repository: BookingRepository,
        transfer_repository: TransferRepository,
        activity_log_repository: ActivityLogRepository,
    ):
        self.assets = asset_repository
        self.allocations = allocation_repository
        self.maintenance = maintenance_repository
        self.bookings = booking_repository
        self.transfers = transfer_repository
        self.activity_logs = activity_log_repository

    async def get_kpis(self):
        available_page = await self.assets.search({"status": "Available"}, skip=0, limit=1)
        allocated_page = await self.assets.search({"status": "Allocated"}, skip=0, limit=1)
        maintenance_today = await self.maintenance.list_due_today()
        upcoming_bookings = await self.bookings.list_upcoming_for_reminders()
        pending_transfers = await self.transfers.list_pending()
        overdue_allocations = await self.allocations.list_overdue()

        return {
            "assets_available": available_page.total,
            "assets_allocated": allocated_page.total,
            "maintenance_today": len(maintenance_today),
            "active_bookings": len(upcoming_bookings),
            "pending_transfers": len(pending_transfers),
            "upcoming_returns": 0,  # requires a dedicated 7-day-window repository query
            "overdue_returns": len(overdue_allocations),
        }

    async def get_recent_activity(self, limit: int = 20):
        page = await self.activity_logs.search(skip=0, limit=limit)
        return page.items
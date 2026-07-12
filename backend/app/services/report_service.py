from __future__ import annotations

from app.repositories.report_repository import ReportRepository


class ReportService:
    def __init__(self, report_repository: ReportRepository):
        self.reports = report_repository

    async def asset_utilization(self):
        return await self.reports.asset_utilization()

    async def department_summary(self):
        return await self.reports.department_summary()

    async def maintenance_summary(self):
        return await self.reports.maintenance_summary()

    async def booking_heatmap(self):
        return await self.reports.booking_heatmap()

    async def idle_assets(self, days: int = 90):
        return await self.reports.idle_assets(days)
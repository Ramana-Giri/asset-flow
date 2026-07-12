from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional

from app.repositories.maintenance_repository import MaintenanceRepository
from app.repositories.asset_repository import AssetRepository
from app.services.asset_service import AssetService
from app.services.notification_service import NotificationService
from app.services.activity_log_service import ActivityLogService
from app.core.exceptions import NotFoundException, PermissionDenied


class MaintenanceService:
    def __init__(
        self,
        maintenance_repository: MaintenanceRepository,
        asset_repository: AssetRepository,
        asset_service: AssetService,
        notification_service: NotificationService,
        activity_log_service: ActivityLogService,
    ):
        self.maintenance = maintenance_repository
        self.assets = asset_repository
        self.asset_service = asset_service
        self.notifications = notification_service
        self.activity_log = activity_log_service

    async def raise_request(
        self, asset_id: int, raised_by: int, issue_description: str, priority: str = "Medium", photo_url: Optional[str] = None
    ):
        asset = await self.assets.find_by_id(asset_id)
        if asset is None:
            raise NotFoundException(f"Asset {asset_id} not found")

        request = await self.maintenance.create(
            {
                "asset_id": asset_id,
                "raised_by": raised_by,
                "issue_description": issue_description,
                "priority": priority,
                "photo_url": photo_url,
                "status": "Pending",
            }
        )
        await self.activity_log.log(
            user_id=raised_by, action="RAISE_MAINTENANCE_REQUEST", entity_type="MaintenanceRequest", entity_id=request.id
        )
        return request

    async def approve_request(self, request_id: int, reviewer_id: int, reviewer_role: str):
        if reviewer_role not in ("Asset Manager", "Admin"):
            raise PermissionDenied("Only an Asset Manager may approve maintenance requests")

        request = await self.maintenance.find_by_id(request_id)
        if request is None:
            raise NotFoundException(f"Maintenance request {request_id} not found")

        now = datetime.now(timezone.utc)
        updated = await self.maintenance.update(
            request_id, {"status": "Approved", "reviewed_by": reviewer_id, "reviewed_at": now}
        )
        await self.asset_service.transition_status(
            request.asset_id, "Under Maintenance", reviewer_id, reference_type="Maintenance", reference_id=request_id
        )
        await self.notifications.notify(
            user_id=request.raised_by,
            type="Maintenance Approved",
            title="Maintenance Approved",
            message=f"Maintenance request #{request_id} has been approved.",
            reference_type="MaintenanceRequest",
            reference_id=request_id,
        )
        await self.activity_log.log(
            user_id=reviewer_id, action="APPROVE_MAINTENANCE", entity_type="MaintenanceRequest", entity_id=request_id
        )
        return updated

    async def reject_request(self, request_id: int, reviewer_id: int, rejection_reason: str):
        request = await self.maintenance.find_by_id(request_id)
        if request is None:
            raise NotFoundException(f"Maintenance request {request_id} not found")

        now = datetime.now(timezone.utc)
        updated = await self.maintenance.update(
            request_id,
            {"status": "Rejected", "rejection_reason": rejection_reason, "reviewed_by": reviewer_id, "reviewed_at": now},
        )
        await self.notifications.notify(
            user_id=request.raised_by,
            type="Maintenance Rejected",
            title="Maintenance Rejected",
            message=f"Maintenance request #{request_id} was rejected: {rejection_reason}",
            reference_type="MaintenanceRequest",
            reference_id=request_id,
        )
        await self.activity_log.log(
            user_id=reviewer_id, action="REJECT_MAINTENANCE", entity_type="MaintenanceRequest", entity_id=request_id
        )
        return updated

    async def assign_technician(
        self, request_id: int, technician_name: str, technician_contact: Optional[str], actor_id: int
    ):
        updated = await self.maintenance.update(
            request_id,
            {
                "technician_name": technician_name,
                "technician_contact": technician_contact,
                "status": "Technician Assigned",
                "technician_assigned_at": datetime.now(timezone.utc),
            },
        )
        if updated is None:
            raise NotFoundException(f"Maintenance request {request_id} not found")
        await self.activity_log.log(
            user_id=actor_id, action="ASSIGN_TECHNICIAN", entity_type="MaintenanceRequest", entity_id=request_id
        )
        return updated

    async def start_progress(self, request_id: int, actor_id: int):
        updated = await self.maintenance.update(
            request_id, {"status": "In Progress", "in_progress_at": datetime.now(timezone.utc)}
        )
        if updated is None:
            raise NotFoundException(f"Maintenance request {request_id} not found")
        await self.activity_log.log(
            user_id=actor_id, action="START_MAINTENANCE_PROGRESS", entity_type="MaintenanceRequest", entity_id=request_id
        )
        return updated

    async def resolve_request(self, request_id: int, resolution_notes: Optional[str], actor_id: int):
        request = await self.maintenance.find_by_id(request_id)
        if request is None:
            raise NotFoundException(f"Maintenance request {request_id} not found")

        updated = await self.maintenance.update(
            request_id,
            {"status": "Resolved", "resolution_notes": resolution_notes, "resolved_at": datetime.now(timezone.utc)},
        )
        await self.asset_service.transition_status(
            request.asset_id, "Available", actor_id, reference_type="Maintenance", reference_id=request_id
        )
        await self.notifications.notify(
            user_id=request.raised_by,
            type="Maintenance Resolved",
            title="Maintenance Resolved",
            message=f"Maintenance request #{request_id} has been resolved.",
            reference_type="MaintenanceRequest",
            reference_id=request_id,
        )
        await self.activity_log.log(
            user_id=actor_id, action="RESOLVE_MAINTENANCE", entity_type="MaintenanceRequest", entity_id=request_id
        )
        return updated

    async def get_maintenance_history(self, asset_id: int):
        return await self.maintenance.list_by_asset(asset_id)
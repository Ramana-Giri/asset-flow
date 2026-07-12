from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional

from app.repositories.audit_repository import AuditRepository
from app.repositories.asset_repository import AssetRepository
from app.repositories.user_repository import UserRepository
from app.services.asset_service import AssetService
from app.services.notification_service import NotificationService
from app.services.activity_log_service import ActivityLogService
from app.core.exceptions import NotFoundException, PermissionDenied, ValidationError


class AuditService:
    def __init__(
        self,
        audit_repository: AuditRepository,
        asset_repository: AssetRepository,
        user_repository: UserRepository,
        asset_service: AssetService,
        notification_service: NotificationService,
        activity_log_service: ActivityLogService,
    ):
        self.audits = audit_repository
        self.assets = asset_repository
        self.users = user_repository
        self.asset_service = asset_service
        self.notifications = notification_service
        self.activity_log = activity_log_service

    async def create_cycle(
        self,
        name: str,
        start_date,
        end_date,
        created_by: int,
        scope_department_id: Optional[int] = None,
        scope_location: Optional[str] = None,
    ):
        if end_date < start_date:
            raise ValidationError("end_date must be on or after start_date")

        cycle = await self.audits.create(
            {
                "name": name,
                "scope_department_id": scope_department_id,
                "scope_location": scope_location,
                "start_date": start_date,
                "end_date": end_date,
                "status": "Planned",
                "created_by": created_by,
            }
        )

        filters: dict = {}
        if scope_department_id is not None:
            filters["department_id"] = scope_department_id
        if scope_location is not None:
            filters["location"] = scope_location
        in_scope_assets = await self.assets.search(filters, skip=0, limit=100000)

        for asset in in_scope_assets.items:
            await self.audits.upsert_item_result(
                audit_cycle_id=cycle.id,
                asset_id=asset.id,
                auditor_id=None,
                result=None,
                remarks=None,
                checked_at=None,
            )

        await self.activity_log.log(
            user_id=created_by, action="CREATE_AUDIT_CYCLE", entity_type="AuditCycle", entity_id=cycle.id
        )
        return cycle

    async def assign_auditors(self, audit_cycle_id: int, auditor_ids: list[int], actor_id: int):
        for auditor_id in auditor_ids:
            user = await self.users.find_by_id(auditor_id)
            if user is None:
                raise NotFoundException(f"User {auditor_id} not found")

        rows = await self.audits.assign_auditors(audit_cycle_id, auditor_ids)
        for auditor_id in auditor_ids:
            await self.notifications.notify(
                user_id=auditor_id,
                type="Auditor Assigned",
                title="You've been assigned to an audit cycle",
                message=f"You are now an auditor for audit cycle #{audit_cycle_id}.",
                reference_type="AuditCycle",
                reference_id=audit_cycle_id,
            )
        await self.activity_log.log(
            user_id=actor_id, action="ASSIGN_AUDITORS", entity_type="AuditCycle", entity_id=audit_cycle_id
        )
        return rows

    async def verify_asset(
        self, audit_cycle_id: int, asset_id: int, auditor_id: int, result: str, remarks: Optional[str] = None
    ):
        item = await self.audits.upsert_item_result(
            audit_cycle_id=audit_cycle_id,
            asset_id=asset_id,
            auditor_id=auditor_id,
            result=result,
            remarks=remarks,
            checked_at=datetime.now(timezone.utc),
        )
        if result != "Verified":
            await self.notifications.notify(
                user_id=auditor_id,
                type="Audit Discrepancy Flagged",
                title="Audit Discrepancy",
                message=f"Asset #{asset_id} was flagged as '{result}' during audit cycle #{audit_cycle_id}.",
                reference_type="AuditItem",
                reference_id=item.id,
            )
        await self.activity_log.log(
            user_id=auditor_id,
            action="VERIFY_AUDIT_ASSET",
            entity_type="AuditItem",
            entity_id=item.id,
            details={"result": result},
        )
        return item

    async def get_discrepancy_report(self, audit_cycle_id: int):
        return await self.audits.list_discrepancies(audit_cycle_id)

    async def resolve_discrepancy(self, item_id: int, resolver_id: int, resolver_role: str):
        if resolver_role not in ("Asset Manager", "Admin"):
            raise PermissionDenied("Only an Asset Manager may resolve audit discrepancies")
        # Direct AuditItem update; AuditRepository exposes upsert_item_result keyed by (cycle, asset),
        # so resolution is applied via the base repository update here.
        from app.db.models.audit_item import AuditItem  # local import to avoid unnecessary top-level coupling

        item = await self.audits.session.get(AuditItem, item_id) if hasattr(self.audits, "session") else None
        if item is None:
            raise NotFoundException(f"Audit item {item_id} not found")
        item.resolution_status = "Resolved"
        item.resolved_by = resolver_id
        item.resolved_at = datetime.now(timezone.utc)
        await self.activity_log.log(
            user_id=resolver_id, action="RESOLVE_AUDIT_DISCREPANCY", entity_type="AuditItem", entity_id=item_id
        )
        return item

    async def close_cycle(self, audit_cycle_id: int, closed_by: int):
        items = await self.audits.list_items_by_cycle(audit_cycle_id)
        if any(item.result is None for item in items):
            raise ValidationError("All assets must be verified before the audit cycle can be closed")

        for item in items:
            if item.result == "Missing" and item.resolution_status == "Open":
                await self.asset_service.transition_status(
                    item.asset_id, "Lost", closed_by, reference_type="Audit", reference_id=item.id
                )

        cycle = await self.audits.close_cycle(audit_cycle_id, closed_by, datetime.now(timezone.utc))
        if cycle is None:
            raise NotFoundException(f"Audit cycle {audit_cycle_id} not found")

        await self.activity_log.log(
            user_id=closed_by, action="CLOSE_AUDIT_CYCLE", entity_type="AuditCycle", entity_id=audit_cycle_id
        )
        return cycle
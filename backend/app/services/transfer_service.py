from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional

from app.repositories.transfer_repository import TransferRepository
from app.repositories.allocation_repository import AllocationRepository
from app.repositories.asset_repository import AssetRepository
from app.services.allocation_service import AllocationService
from app.services.notification_service import NotificationService
from app.services.activity_log_service import ActivityLogService
from app.core.exceptions import NotFoundException, TransferNotAllowed, PermissionDenied


class TransferService:
    def __init__(
        self,
        transfer_repository: TransferRepository,
        allocation_repository: AllocationRepository,
        asset_repository: AssetRepository,
        allocation_service: AllocationService,
        notification_service: NotificationService,
        activity_log_service: ActivityLogService,
    ):
        self.transfers = transfer_repository
        self.allocations = allocation_repository
        self.assets = asset_repository
        self.allocation_service = allocation_service
        self.notifications = notification_service
        self.activity_log = activity_log_service

    async def request_transfer(
        self,
        asset_id: int,
        requested_by: int,
        to_user_id: Optional[int] = None,
        to_department_id: Optional[int] = None,
        reason: Optional[str] = None,
    ):
        active_allocation = await self.allocations.find_active_by_asset(asset_id)
        if active_allocation is None:
            raise TransferNotAllowed(f"Asset {asset_id} has no active allocation to transfer")
        if not to_user_id and not to_department_id:
            raise TransferNotAllowed("Either to_user_id or to_department_id must be provided")

        transfer = await self.transfers.create(
            {
                "asset_id": asset_id,
                "from_allocation_id": active_allocation.id,
                "requested_by": requested_by,
                "to_user_id": to_user_id,
                "to_department_id": to_department_id,
                "reason": reason,
                "status": "Requested",
            }
        )
        await self.activity_log.log(
            user_id=requested_by, action="REQUEST_TRANSFER", entity_type="TransferRequest", entity_id=transfer.id
        )
        return transfer

    async def approve_transfer(self, transfer_id: int, approver_id: int, approver_role: str):
        if approver_role not in ("Asset Manager", "Department Head", "Admin"):
            raise PermissionDenied("Only an Asset Manager or Department Head may approve transfers")

        transfer = await self.transfers.find_by_id(transfer_id)
        if transfer is None:
            raise NotFoundException(f"Transfer request {transfer_id} not found")

        now = datetime.now(timezone.utc)
        await self.transfers.mark_decision(transfer_id, "Approved", approver_id, now)

        await self.allocation_service.return_asset(transfer.asset_id, approver_id)
        new_allocation = await self.allocation_service.allocate_asset(
            asset_id=transfer.asset_id,
            allocated_to_type="Employee" if transfer.to_user_id else "Department",
            allocated_by=approver_id,
            allocated_to_user_id=transfer.to_user_id,
            allocated_to_department_id=transfer.to_department_id,
        )
        completed = await self.transfers.mark_completed(transfer_id, new_allocation.id)

        recipient_ids = [uid for uid in (transfer.requested_by, transfer.to_user_id) if uid]
        for uid in recipient_ids:
            await self.notifications.notify(
                user_id=uid,
                type="Transfer Approved",
                title="Transfer Approved",
                message=f"Transfer request #{transfer_id} has been approved and completed.",
                reference_type="TransferRequest",
                reference_id=transfer_id,
            )

        await self.activity_log.log(
            user_id=approver_id, action="APPROVE_TRANSFER", entity_type="TransferRequest", entity_id=transfer_id
        )
        return completed

    async def reject_transfer(self, transfer_id: int, approver_id: int):
        transfer = await self.transfers.find_by_id(transfer_id)
        if transfer is None:
            raise NotFoundException(f"Transfer request {transfer_id} not found")

        now = datetime.now(timezone.utc)
        updated = await self.transfers.mark_decision(transfer_id, "Rejected", approver_id, now)

        await self.notifications.notify(
            user_id=transfer.requested_by,
            type="Transfer Rejected",
            title="Transfer Rejected",
            message=f"Transfer request #{transfer_id} was rejected.",
            reference_type="TransferRequest",
            reference_id=transfer_id,
        )
        await self.activity_log.log(
            user_id=approver_id, action="REJECT_TRANSFER", entity_type="TransferRequest", entity_id=transfer_id
        )
        return updated

    async def get_transfer_history(self, asset_id: int):
        return await self.transfers.list_by_asset(asset_id)
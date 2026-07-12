from __future__ import annotations
from typing import Optional

from app.repositories.notification_repository import NotificationRepository


class NotificationService:
    def __init__(self, notification_repository: NotificationRepository):
        self.notifications = notification_repository

    async def notify(
        self,
        user_id: int,
        type: str,
        title: str,
        message: str,
        reference_type: Optional[str] = None,
        reference_id: Optional[int] = None,
    ):
        return await self.notifications.create(
            {
                "user_id": user_id,
                "type": type,
                "title": title,
                "message": message,
                "reference_type": reference_type,
                "reference_id": reference_id,
            }
        )

    async def notify_asset_allocated(self, user_id: int, asset_id: int, allocation_id: int):
        return await self.notify(
            user_id=user_id,
            type="Asset Assigned",
            title="Asset Assigned",
            message=f"Asset #{asset_id} has been assigned to you.",
            reference_type="Allocation",
            reference_id=allocation_id,
        )

    async def notify_transfer_approved(self, user_id: int, transfer_id: int):
        return await self.notify(
            user_id=user_id,
            type="Transfer Approved",
            title="Transfer Approved",
            message=f"Transfer request #{transfer_id} has been approved.",
            reference_type="TransferRequest",
            reference_id=transfer_id,
        )

    async def notify_maintenance_status_changed(self, user_id: int, request_id: int, status: str):
        type_map = {
            "Approved": "Maintenance Approved",
            "Rejected": "Maintenance Rejected",
            "Resolved": "Maintenance Resolved",
        }
        notif_type = type_map.get(status, "Maintenance Approved")
        return await self.notify(
            user_id=user_id,
            type=notif_type,
            title=notif_type,
            message=f"Maintenance request #{request_id} status changed to {status}.",
            reference_type="MaintenanceRequest",
            reference_id=request_id,
        )

    async def notify_booking_event(self, user_id: int, booking_id: int, event: str):
        type_map = {
            "confirmed": "Booking Confirmed",
            "cancelled": "Booking Cancelled",
            "reminder": "Booking Reminder",
        }
        notif_type = type_map.get(event, "Booking Confirmed")
        return await self.notify(
            user_id=user_id,
            type=notif_type,
            title=notif_type,
            message=f"Booking #{booking_id}: {notif_type}.",
            reference_type="Booking",
            reference_id=booking_id,
        )

    async def notify_audit_discrepancy(self, user_id: int, audit_item_id: int, asset_id: int, result: str):
        return await self.notify(
            user_id=user_id,
            type="Audit Discrepancy Flagged",
            title="Audit Discrepancy",
            message=f"Asset #{asset_id} was flagged as '{result}'.",
            reference_type="AuditItem",
            reference_id=audit_item_id,
        )

    async def notify_overdue_return(self, user_id: int, allocation_id: int, asset_id: int):
        return await self.notify(
            user_id=user_id,
            type="Overdue Return Alert",
            title="Overdue Asset Return",
            message=f"Asset #{asset_id} is overdue for return.",
            reference_type="Allocation",
            reference_id=allocation_id,
        )

    async def list_for_user(self, user_id: int, skip: int = 0, limit: int = 50):
        page = await self.notifications.list_by_user(user_id, skip, limit)
        unread_count = await self.notifications.count_unread(user_id)
        return {"items": page.items, "total": page.total, "skip": page.skip, "limit": page.limit, "unread_count": unread_count}

    async def mark_read(self, notification_ids: list[int]):
        return await self.notifications.mark_read(notification_ids)
from __future__ import annotations
from datetime import date
from typing import Optional

from app.repositories.allocation_repository import AllocationRepository
from app.repositories.asset_repository import AssetRepository
from app.services.asset_service import AssetService
from app.services.notification_service import NotificationService
from app.services.activity_log_service import ActivityLogService
from app.core.exceptions import NotFoundException, AssetAlreadyAllocated, ValidationError


class AllocationService:
    def __init__(
        self,
        allocation_repository: AllocationRepository,
        asset_repository: AssetRepository,
        asset_service: AssetService,
        notification_service: NotificationService,
        activity_log_service: ActivityLogService,
    ):
        self.allocations = allocation_repository
        self.assets = asset_repository
        self.asset_service = asset_service
        self.notifications = notification_service
        self.activity_log = activity_log_service

    async def allocate_asset(
        self,
        asset_id: int,
        allocated_to_type: str,
        allocated_by: int,
        allocated_to_user_id: Optional[int] = None,
        allocated_to_department_id: Optional[int] = None,
        expected_return_date: Optional[date] = None,
    ):
        asset = await self.assets.find_by_id(asset_id)
        if asset is None:
            raise NotFoundException(f"Asset {asset_id} not found")

        existing_active = await self.allocations.find_active_by_asset(asset_id)
        if existing_active is not None:
            raise AssetAlreadyAllocated(
                f"Asset {asset_id} is currently held by "
                f"{'user ' + str(existing_active.allocated_to_user_id) if existing_active.allocated_to_user_id else 'department ' + str(existing_active.allocated_to_department_id)}. "
                "Consider a Transfer Request instead."
            )

        allocation = await self.allocations.create(
            {
                "asset_id": asset_id,
                "allocated_to_type": allocated_to_type,
                "allocated_to_user_id": allocated_to_user_id,
                "allocated_to_department_id": allocated_to_department_id,
                "allocated_by": allocated_by,
                "expected_return_date": expected_return_date,
            }
        )

        await self.asset_service.transition_status(
            asset_id, "Allocated", allocated_by, reference_type="Allocation", reference_id=allocation.id
        )

        recipient_id = allocated_to_user_id
        if recipient_id:
            await self.notifications.notify(
                user_id=recipient_id,
                type="Asset Assigned",
                title="Asset Assigned",
                message=f"Asset #{asset_id} has been assigned to you.",
                reference_type="Allocation",
                reference_id=allocation.id,
            )

        await self.activity_log.log(
            user_id=allocated_by,
            action="ALLOCATE_ASSET",
            entity_type="Allocation",
            entity_id=allocation.id,
            details={"asset_id": asset_id},
        )
        return allocation

    async def return_asset(self, asset_id: int, returned_by: int, return_condition_notes: Optional[str] = None):
        allocation = await self.allocations.find_active_by_asset(asset_id)
        if allocation is None:
            raise ValidationError(f"Asset {asset_id} has no active allocation to return")

        updated = await self.allocations.mark_returned(
            allocation.id, date.today(), return_condition_notes, returned_by
        )

        await self.asset_service.transition_status(
            asset_id, "Available", returned_by, reference_type="Allocation", reference_id=allocation.id
        )

        recipient_id = allocation.allocated_to_user_id
        if recipient_id:
            await self.notifications.notify(
                user_id=recipient_id,
                type="Asset Returned",
                title="Asset Return Confirmed",
                message=f"Return of asset #{asset_id} has been recorded.",
                reference_type="Allocation",
                reference_id=allocation.id,
            )

        await self.activity_log.log(
            user_id=returned_by,
            action="RETURN_ASSET",
            entity_type="Allocation",
            entity_id=allocation.id,
            details={"asset_id": asset_id},
        )
        return updated

    async def list_overdue_allocations(self):
        return await self.allocations.list_overdue()

    async def get_allocation_history(
        self, asset_id: Optional[int] = None, user_id: Optional[int] = None, department_id: Optional[int] = None
    ):
        if user_id is not None:
            return await self.allocations.list_by_user(user_id)
        if department_id is not None:
            return await self.allocations.list_by_department(department_id)
        raise ValidationError("Provide either user_id or department_id (or use AssetService.get_asset_history)")

    async def notify_overdue_returns(self):
        overdue = await self.allocations.list_overdue()
        for allocation in overdue:
            if allocation.allocated_to_user_id:
                await self.notifications.notify(
                    user_id=allocation.allocated_to_user_id,
                    type="Overdue Return Alert",
                    title="Overdue Asset Return",
                    message=f"Asset #{allocation.asset_id} was due back on {allocation.expected_return_date}.",
                    reference_type="Allocation",
                    reference_id=allocation.id,
                )
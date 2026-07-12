from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user, get_current_asset_manager
from app.core.responses import success
from app.repositories.audit_repository import AuditRepository
from app.repositories.asset_repository import AssetRepository
from app.repositories.asset_category_repository import AssetCategoryRepository
from app.repositories.department_repository import DepartmentRepository
from app.repositories.allocation_repository import AllocationRepository
from app.repositories.maintenance_repository import MaintenanceRepository
from app.repositories.user_repository import UserRepository
from app.repositories.activity_log_repository import ActivityLogRepository
from app.repositories.notification_repository import NotificationRepository
from app.services.audit_service import AuditService
from app.services.asset_service import AssetService
from app.services.notification_service import NotificationService
from app.services.activity_log_service import ActivityLogService
from app.schemas.audit import AuditCycleCreate, AuditorAssign, AuditItemVerify, AuditDiscrepancyResolve

router = APIRouter(prefix="/audits", tags=["Audits"])


def get_audit_service(db: AsyncSession = Depends(get_db)) -> AuditService:
    asset_service = AssetService(
        AssetRepository(db),
        AssetCategoryRepository(db),
        DepartmentRepository(db),
        AllocationRepository(db),
        MaintenanceRepository(db),
        ActivityLogService(ActivityLogRepository(db)),
    )
    return AuditService(
        AuditRepository(db),
        AssetRepository(db),
        UserRepository(db),
        asset_service,
        NotificationService(NotificationRepository(db)),
        ActivityLogService(ActivityLogRepository(db)),
    )


@router.post("")
async def create_cycle(
    payload: AuditCycleCreate, service: AuditService = Depends(get_audit_service), actor=Depends(get_current_asset_manager)
):
    cycle = await service.create_cycle(
        payload.name, payload.start_date, payload.end_date, actor.id, payload.scope_department_id, payload.scope_location
    )
    return success(data=cycle, message="Audit cycle created")


@router.post("/{audit_cycle_id}/auditors")
async def assign_auditors(
    audit_cycle_id: int, payload: AuditorAssign, service: AuditService = Depends(get_audit_service), actor=Depends(get_current_asset_manager)
):
    rows = await service.assign_auditors(audit_cycle_id, payload.auditor_ids, actor.id)
    return success(data=rows, message="Auditors assigned")


@router.post("/{audit_cycle_id}/verify")
async def verify_asset(
    audit_cycle_id: int, payload: AuditItemVerify, service: AuditService = Depends(get_audit_service), actor=Depends(get_current_user)
):
    item = await service.verify_asset(audit_cycle_id, payload.asset_id, actor.id, payload.result, payload.remarks)
    return success(data=item, message="Asset verified")


@router.get("/{audit_cycle_id}/discrepancies")
async def get_discrepancy_report(audit_cycle_id: int, service: AuditService = Depends(get_audit_service)):
    items = await service.get_discrepancy_report(audit_cycle_id)
    return success(data=items)


@router.patch("/items/{item_id}/resolve")
async def resolve_discrepancy(
    item_id: int,
    payload: AuditDiscrepancyResolve,
    service: AuditService = Depends(get_audit_service),
    actor=Depends(get_current_asset_manager),
):
    item = await service.resolve_discrepancy(item_id, actor.id, actor.role)
    return success(data=item, message="Discrepancy resolved")


@router.patch("/{audit_cycle_id}/close")
async def close_cycle(
    audit_cycle_id: int, service: AuditService = Depends(get_audit_service), actor=Depends(get_current_asset_manager)
):
    cycle = await service.close_cycle(audit_cycle_id, actor.id)
    return success(data=cycle, message="Audit cycle closed")
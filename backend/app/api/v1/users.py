from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user, get_current_admin
from app.core.responses import success
from app.repositories.user_repository import UserRepository
from app.repositories.activity_log_repository import ActivityLogRepository
from app.repositories.notification_repository import NotificationRepository
from app.services.user_service import UserService
from app.services.activity_log_service import ActivityLogService
from app.services.notification_service import NotificationService
from app.schemas.user import UserCreate, UserUpdate, UserRoleUpdate, UserFilter

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(
        UserRepository(db),
        ActivityLogService(ActivityLogRepository(db)),
        NotificationService(NotificationRepository(db)),
    )


@router.get("")
async def list_users(
    filters: UserFilter = Depends(), skip: int = 0, limit: int = 50, service: UserService = Depends(get_user_service)
):
    page = await service.list_users(filters.model_dump(exclude_none=True), skip, limit)
    return success(data={"items": page.items, "total": page.total, "skip": page.skip, "limit": page.limit})


@router.get("/{user_id}")
async def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    user = await service.get_user(user_id)
    return success(data=user)


@router.post("")
async def create_user(payload: UserCreate, service: UserService = Depends(get_user_service), admin=Depends(get_current_admin)):
    user = await service.create_user(payload.name, payload.email, payload.password, payload.department_id, admin.id)
    return success(data=user, message="User created")


@router.put("/{user_id}")
async def update_user(
    user_id: int, payload: UserUpdate, service: UserService = Depends(get_user_service), actor=Depends(get_current_user)
):
    user = await service.update_user(user_id, payload.model_dump(exclude_none=True), actor.id)
    return success(data=user, message="User updated")


@router.patch("/{user_id}/department")
async def assign_department(
    user_id: int, department_id: int, service: UserService = Depends(get_user_service), actor=Depends(get_current_user)
):
    user = await service.set_department(user_id, department_id, actor.id)
    return success(data=user, message="Department assigned")


@router.patch("/{user_id}/role")
async def promote_role(
    user_id: int, payload: UserRoleUpdate, service: UserService = Depends(get_user_service), admin=Depends(get_current_admin)
):
    user = await service.promote_role(user_id, payload.role, {"role": admin.role}, admin.id)
    return success(data=user, message="Role updated")


@router.patch("/{user_id}/activate")
async def activate_user(user_id: int, service: UserService = Depends(get_user_service), admin=Depends(get_current_admin)):
    user = await service.activate_user(user_id, admin.id)
    return success(data=user, message="User activated")


@router.patch("/{user_id}/deactivate")
async def deactivate_user(user_id: int, service: UserService = Depends(get_user_service), admin=Depends(get_current_admin)):
    user = await service.deactivate_user(user_id, admin.id)
    return success(data=user, message="User deactivated")
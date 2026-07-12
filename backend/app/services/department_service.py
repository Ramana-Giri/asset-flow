from __future__ import annotations
from typing import Optional

from app.repositories.department_repository import DepartmentRepository
from app.repositories.user_repository import UserRepository
from app.core.exceptions import NotFoundException, ValidationError, CircularDepartmentHierarchy
from app.services.activity_log_service import ActivityLogService
from app.services.notification_service import NotificationService


class DepartmentService:
    def __init__(
        self,
        department_repository: DepartmentRepository,
        user_repository: UserRepository,
        activity_log_service: ActivityLogService,
        notification_service: NotificationService,
    ):
        self.departments = department_repository
        self.users = user_repository
        self.activity_log = activity_log_service
        self.notifications = notification_service

    async def list_departments(self, filters: dict, skip: int = 0, limit: int = 50):
        return await self.departments.search(filters, skip, limit)

    async def get_department(self, department_id: int):
        department = await self.departments.find_by_id(department_id)
        if department is None:
            raise NotFoundException(f"Department {department_id} not found")
        return department

    async def create_department(
        self, name: str, parent_department_id: Optional[int], head_user_id: Optional[int], actor_id: int
    ):
        existing = await self.departments.find_by_name(name)
        if existing is not None:
            raise ValidationError("Department name must be unique")
        if parent_department_id is not None:
            parent = await self.departments.find_by_id(parent_department_id)
            if parent is None:
                raise NotFoundException(f"Parent department {parent_department_id} not found")
        if head_user_id is not None:
            head = await self.users.find_by_id(head_user_id)
            if head is None:
                raise NotFoundException(f"User {head_user_id} not found")

        department = await self.departments.create(
            {"name": name, "parent_department_id": parent_department_id, "head_user_id": head_user_id}
        )
        await self.activity_log.log(
            user_id=actor_id, action="CREATE_DEPARTMENT", entity_type="Department", entity_id=department.id
        )
        return department

    async def update_department(self, department_id: int, data: dict, actor_id: int):
        new_parent_id = data.get("parent_department_id")
        if new_parent_id is not None:
            if await self.departments.exists_cycle(department_id, new_parent_id):
                raise CircularDepartmentHierarchy(
                    "This change would create a circular department hierarchy"
                )
        department = await self.departments.update(department_id, data)
        if department is None:
            raise NotFoundException(f"Department {department_id} not found")
        await self.activity_log.log(
            user_id=actor_id,
            action="UPDATE_DEPARTMENT",
            entity_type="Department",
            entity_id=department_id,
            details=data,
        )
        return department

    async def assign_head(self, department_id: int, head_user_id: int, actor_id: int):
        user = await self.users.find_by_id(head_user_id)
        if user is None:
            raise NotFoundException(f"User {head_user_id} not found")
        if user.status != "Active":
            raise ValidationError("Cannot assign an inactive user as Department Head")

        department = await self.departments.update(department_id, {"head_user_id": head_user_id})
        if department is None:
            raise NotFoundException(f"Department {department_id} not found")

        await self.notifications.notify(
            user_id=head_user_id,
            type="Department Head Assigned",
            title="You are now a Department Head",
            message=f"You have been assigned as head of {department.name}.",
            reference_type="Department",
            reference_id=department_id,
        )
        await self.activity_log.log(
            user_id=actor_id,
            action="ASSIGN_DEPARTMENT_HEAD",
            entity_type="Department",
            entity_id=department_id,
            details={"head_user_id": head_user_id},
        )
        return department

    async def deactivate_department(self, department_id: int, actor_id: int):
        department = await self.departments.update(department_id, {"status": "Inactive"})
        if department is None:
            raise NotFoundException(f"Department {department_id} not found")
        await self.activity_log.log(
            user_id=actor_id, action="DEACTIVATE_DEPARTMENT", entity_type="Department", entity_id=department_id
        )
        return department
from __future__ import annotations
from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository
from app.db.models.department import Department


class DepartmentRepository(BaseRepository[Department]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Department)

    async def find_by_name(self, name: str) -> Optional[Department]:
        result = await self.session.execute(select(Department).where(Department.name == name))
        return result.scalar_one_or_none()

    async def list_children(self, parent_department_id: int) -> Sequence[Department]:
        result = await self.session.execute(
            select(Department).where(Department.parent_department_id == parent_department_id)
        )
        return result.scalars().all()

    async def exists_cycle(self, department_id: int, new_parent_id: Optional[int]) -> bool:
        """Walk up from new_parent_id; True if department_id is encountered (would create a cycle)."""
        current_id = new_parent_id
        visited = set()
        while current_id is not None:
            if current_id == department_id:
                return True
            if current_id in visited:
                break
            visited.add(current_id)
            dept = await self.find_by_id(current_id)
            if dept is None:
                break
            current_id = dept.parent_department_id
        return False
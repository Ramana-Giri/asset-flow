from __future__ import annotations
from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository
from app.db.models.user import User


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def find_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def list_by_department(self, department_id: int) -> Sequence[User]:
        result = await self.session.execute(select(User).where(User.department_id == department_id))
        return result.scalars().all()

    async def update_role(self, user_id: int, role: str, promoted_by: int, promoted_at) -> Optional[User]:
        user = await self.find_by_id(user_id)
        if user is None:
            return None
        user.role = role
        user.promoted_by = promoted_by
        user.promoted_at = promoted_at
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def set_status(self, user_id: int, status: str) -> Optional[User]:
        user = await self.find_by_id(user_id)
        if user is None:
            return None
        user.status = status
        await self.session.flush()
        await self.session.refresh(user)
        return user
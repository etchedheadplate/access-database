from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Group, Permission, Resource, User


class AccessCheckService:
    @staticmethod
    async def check_user_in_group(db: AsyncSession, user_id: UUID, group_id: int) -> bool:
        query = select(Group).join(Group.users).where(Group.id == group_id, User.id == user_id)  # type: ignore[arg-type]
        result = await db.execute(query)
        return result.scalars().first() is not None

    @staticmethod
    async def check_permission_in_group(db: AsyncSession, permission_id: int, group_id: int) -> bool:
        query = select(Group).join(Group.permissions).where(Group.id == group_id, Permission.id == permission_id)
        result = await db.execute(query)
        return result.scalars().first() is not None

    @staticmethod
    async def check_resource_in_permission(db: AsyncSession, resource_id: int, permission_id: int) -> bool:
        query = (
            select(Permission)
            .join(Permission.resources)
            .where(Permission.id == permission_id, Resource.id == resource_id)
        )
        result = await db.execute(query)
        return result.scalars().first() is not None

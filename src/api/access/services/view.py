from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Group, Permission, Resource, User


class AccessViewService:
    @staticmethod
    async def view_group_users(db: AsyncSession, group_id: int) -> bool:
        query = select(User).join(User.groups).where(Group.id == group_id)
        result = await db.execute(query)
        return result.scalars().all()  # type: ignore[arg-type]

    @staticmethod
    async def view_group_permissions(db: AsyncSession, group_id: int) -> bool:
        query = select(Permission).join(Permission.groups).where(Group.id == group_id)
        result = await db.execute(query)
        return result.scalars().all()  # type: ignore[arg-type]

    @staticmethod
    async def view_permission_resources(db: AsyncSession, permission_id: int) -> bool:
        query = select(Resource).join(Resource.permissions).where(Permission.id == permission_id)
        result = await db.execute(query)
        return result.scalars().all()  # type: ignore[arg-type]

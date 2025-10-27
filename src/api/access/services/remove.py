from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import Group, Permission, Resource, User


class AccessRemoveService:
    @staticmethod
    async def remove_user_from_group(db: AsyncSession, user_id: UUID, group_id: int) -> bool:
        query = select(Group).options(selectinload(Group.users)).where(Group.id == group_id)
        result = await db.execute(query)
        group = result.scalars().first()
        if not group:
            return False

        user = await db.get(User, user_id)
        if not user or user not in group.users:
            return False

        group.users.remove(user)
        await db.commit()
        return True

    @staticmethod
    async def remove_permission_from_group(db: AsyncSession, permission_id: int, group_id: int) -> bool:
        query = select(Group).options(selectinload(Group.permissions)).where(Group.id == group_id)
        result = await db.execute(query)
        group = result.scalars().first()
        if not group:
            return False

        permission = await db.get(Permission, permission_id)
        if not permission or permission not in group.permissions:
            return False

        group.permissions.remove(permission)
        await db.commit()
        return True

    @staticmethod
    async def remove_resource_from_permission(db: AsyncSession, resource_id: int, permission_id: int) -> bool:
        query = select(Permission).options(selectinload(Permission.resources)).where(Permission.id == permission_id)
        result = await db.execute(query)
        permission = result.scalars().first()
        if not permission:
            return False

        resource = await db.get(Resource, resource_id)
        if not resource or resource not in permission.resources:
            return False

        permission.resources.remove(resource)
        await db.commit()
        return True

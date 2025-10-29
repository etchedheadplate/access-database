from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Group, Permission, Resource, User


class AccessViewService:
    @staticmethod
    async def view_user_groups(db: AsyncSession, user_id: UUID):
        query = select(Group).join(Group.users).where(User.id == user_id)  # type: ignore[arg-type]
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def view_user_permissions(db: AsyncSession, user_id: UUID):
        query = (
            select(Permission)
            .join(Permission.groups)
            .join(Group.users)
            .where(User.id == user_id)  # type: ignore[arg-type]
        )
        result = await db.execute(query)
        return result.scalars().unique().all()

    @staticmethod
    async def view_user_resources(db: AsyncSession, user_id: UUID):
        query = (
            select(Resource)
            .join(Resource.permissions)
            .join(Permission.groups)
            .join(Group.users)
            .where(User.id == user_id)  # type: ignore[arg-type]
        )
        result = await db.execute(query)
        return result.scalars().unique().all()

    @staticmethod
    async def view_group_users(db: AsyncSession, group_id: int):
        query = select(User).join(User.groups).where(Group.id == group_id)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def view_group_permissions(db: AsyncSession, group_id: int):
        query = select(Permission).join(Permission.groups).where(Group.id == group_id)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def view_group_resources(db: AsyncSession, group_id: int):
        query = select(Resource).join(Resource.permissions).join(Permission.groups).where(Group.id == group_id)
        result = await db.execute(query)
        return result.scalars().unique().all()

    @staticmethod
    async def view_permission_groups(db: AsyncSession, permission_id: int):
        query = select(Group).join(Group.permissions).where(Permission.id == permission_id)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def view_permission_users(db: AsyncSession, permission_id: int):
        query = select(User).join(User.groups).join(Group.permissions).where(Permission.id == permission_id)
        result = await db.execute(query)
        return result.scalars().unique().all()

    @staticmethod
    async def view_permission_resources(db: AsyncSession, permission_id: int):
        query = select(Resource).join(Resource.permissions).where(Permission.id == permission_id)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def view_resource_permissions(db: AsyncSession, resource_id: int):
        """Показать, в какие permissions входит ресурс"""
        query = select(Permission).join(Permission.resources).where(Resource.id == resource_id)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def view_resource_groups(db: AsyncSession, resource_id: int):
        """Показать, через какие группы ресурс доступен"""
        query = select(Group).join(Group.permissions).join(Permission.resources).where(Resource.id == resource_id)
        result = await db.execute(query)
        return result.scalars().unique().all()

    @staticmethod
    async def view_resource_users(db: AsyncSession, resource_id: int):
        """Показать, какие пользователи имеют доступ к ресурсу"""
        query = (
            select(User)
            .join(User.groups)
            .join(Group.permissions)
            .join(Permission.resources)
            .where(Resource.id == resource_id)
        )
        result = await db.execute(query)
        return result.scalars().unique().all()

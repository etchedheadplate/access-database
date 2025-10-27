from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import Group, Permission


class PermissionService:
    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(select(Permission))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, permission_id: int):
        result = await db.execute(select(Permission).where(Permission.id == permission_id))
        return result.scalars().first()

    @staticmethod
    async def create(db: AsyncSession, name: str):
        existing = await db.execute(select(Permission).where(Permission.name == name))
        if existing.scalars().first():
            return None
        permission = Permission(name=name)
        db.add(permission)
        await db.commit()
        await db.refresh(permission)
        return permission

    @staticmethod
    async def link_to_group(db: AsyncSession, permission_id: int, group_id: int):
        result_permission = await db.execute(select(Permission).where(Permission.id == permission_id))
        permission = result_permission.scalars().first()

        result_group = await db.execute(
            select(Group).options(selectinload(Group.permissions)).where(Group.id == group_id)
        )
        group = result_group.scalars().first()

        if not permission or not group:
            return None, None, False

        already_linked = permission in group.permissions

        if not already_linked:
            group.permissions.append(permission)
            await db.commit()
            await db.refresh(group)

        return permission, group, already_linked

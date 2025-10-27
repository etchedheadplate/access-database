from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

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


class AccessGrantService:
    @staticmethod
    async def add_user_to_group(db: AsyncSession, group_id: int, user_id: UUID):
        result_group = await db.execute(select(Group).options(selectinload(Group.users)).where(Group.id == group_id))
        group = result_group.scalars().first()

        result_user = await db.execute(select(User).where(User.id == user_id))  # type: ignore[arg-type]
        user = result_user.scalars().first()

        if not group or not user:
            return None, None, False

        already_in_group = any(u.id == user.id for u in group.users)

        if not already_in_group:
            group.users.append(user)
            await db.commit()
            await db.refresh(group)

        return group, user, already_in_group

    @staticmethod
    async def grant_permission_to_group(db: AsyncSession, permission_id: int, group_id: int):
        result_permission = await db.execute(select(Permission).where(Permission.id == permission_id))
        permission = result_permission.scalars().first()

        result_group = await db.execute(
            select(Group).options(selectinload(Group.permissions)).where(Group.id == group_id)
        )
        group = result_group.scalars().first()

        if not permission or not group:
            return None, None, False

        already_granted = permission in group.permissions

        if not already_granted:
            group.permissions.append(permission)
            await db.commit()
            await db.refresh(group)

        return permission, group, already_granted

    @staticmethod
    async def link_resource_to_permission(db: AsyncSession, resource_id: int, permission_id: int):
        result_resource = await db.execute(select(Resource).where(Resource.id == resource_id))
        resource = result_resource.scalars().first()

        result_permission = await db.execute(
            select(Permission).options(selectinload(Permission.resources)).where(Permission.id == permission_id)
        )
        permission = result_permission.scalars().first()

        if not resource or not permission:
            return None, None, False

        already_linked = resource in permission.resources

        if not already_linked:
            permission.resources.append(resource)
            await db.commit()
            await db.refresh(permission)

        return resource, permission, already_linked

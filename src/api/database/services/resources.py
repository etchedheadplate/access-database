from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import Permission, Resource


class ResourceService:
    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(select(Resource))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, resource_id: int):
        result = await db.execute(select(Resource).where(Resource.id == resource_id))
        return result.scalars().first()

    @staticmethod
    async def create(db: AsyncSession, name: str):
        existing = await db.execute(select(Resource).where(Resource.name == name))
        if existing.scalars().first():
            return None
        resource = Resource(name=name)
        db.add(resource)
        await db.commit()
        await db.refresh(resource)
        return resource

    @staticmethod
    async def link_to_permission(db: AsyncSession, resource_id: int, permission_id: int):
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

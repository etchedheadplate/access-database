from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import Access, Resource


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
    async def link_to_access(db: AsyncSession, resource_id: int, access_id: int):
        result_resource = await db.execute(select(Resource).where(Resource.id == resource_id))
        resource = result_resource.scalars().first()

        result_access = await db.execute(
            select(Access).options(selectinload(Access.resources)).where(Access.id == access_id)
        )
        access = result_access.scalars().first()

        if not resource or not access:
            return None, None, False

        already_linked = resource in access.resources

        if not already_linked:
            access.resources.append(resource)
            await db.commit()
            await db.refresh(access)

        return resource, access, already_linked

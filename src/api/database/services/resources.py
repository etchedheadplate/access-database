from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Resource


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

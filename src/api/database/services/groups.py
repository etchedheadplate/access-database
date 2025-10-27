from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Group


class GroupService:
    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(select(Group))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, group_id: int):
        result = await db.execute(select(Group).where(Group.id == group_id))
        return result.scalars().first()

    @staticmethod
    async def create(db: AsyncSession, name: str):
        existing = await db.execute(select(Group).where(Group.name == name))
        if existing.scalars().first():
            return None
        group = Group(name=name)
        db.add(group)
        await db.commit()
        await db.refresh(group)
        return group

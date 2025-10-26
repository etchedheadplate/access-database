from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import Access, Group


class AccessService:
    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(select(Access))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, access_id: int):
        result = await db.execute(select(Access).where(Access.id == access_id))
        return result.scalars().first()

    @staticmethod
    async def create(db: AsyncSession, name: str):
        existing = await db.execute(select(Access).where(Access.name == name))
        if existing.scalars().first():
            return None
        access = Access(name=name)
        db.add(access)
        await db.commit()
        await db.refresh(access)
        return access

    @staticmethod
    async def link_to_group(db: AsyncSession, access_id: int, group_id: int):
        result_access = await db.execute(select(Access).where(Access.id == access_id))
        access = result_access.scalars().first()

        result_group = await db.execute(select(Group).options(selectinload(Group.accesses)).where(Group.id == group_id))
        group = result_group.scalars().first()

        if not access or not group:
            return None, None, False

        already_linked = access in group.accesses

        if not already_linked:
            group.accesses.append(access)
            await db.commit()
            await db.refresh(group)

        return access, group, already_linked

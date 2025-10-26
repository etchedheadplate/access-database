from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import Group, User


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

    @staticmethod
    async def add_user(db: AsyncSession, group_id: int, user_id: UUID):
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

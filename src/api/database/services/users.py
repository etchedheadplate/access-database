from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User


class UserService:
    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(select(User))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: UUID):
        result = await db.execute(select(User).where(User.id == user_id))  # type: ignore[arg-type]
        return result.scalars().first()

    @staticmethod
    async def create(db: AsyncSession, user_data: dict[str, Any]):
        user = User(**user_data)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def delete(db: AsyncSession, user_id: UUID):
        result = await db.execute(select(User).where(User.id == user_id))  # type: ignore[arg-type]
        user = result.scalars().first()
        if user:
            await db.delete(user)
            await db.commit()
        return user

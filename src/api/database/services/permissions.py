from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Permission


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

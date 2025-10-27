from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.database.schemas.users import UserResponse
from src.api.database.services.users import UserService
from src.database.connection import get_async_session

router = APIRouter(prefix="/users")


@router.get("/", response_model=list[UserResponse])
async def list_users(session: AsyncSession = Depends(get_async_session)):
    service = UserService()
    return await service.get_all(session)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID, session: AsyncSession = Depends(get_async_session)):
    service = UserService()
    user = await service.get_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

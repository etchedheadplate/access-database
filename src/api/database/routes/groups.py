from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.database.schemas.groups import GroupCreateResponse, GroupResponse
from src.api.database.services.groups import GroupService
from src.auth.manager import current_active_user
from src.database.connection import get_async_session
from src.database.models import User

router = APIRouter(prefix="/groups")


@router.get("/", response_model=list[GroupResponse])
async def list_groups(session: AsyncSession = Depends(get_async_session)):
    service = GroupService()
    return await service.get_all(session)


@router.post("/create", response_model=GroupCreateResponse)
async def create_group(
    name: str, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_active_user)
):
    service = GroupService()
    group = await service.create(session, name)

    if not group:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Group with this name already exists")

    return GroupCreateResponse(
        message="Group successfully created",
        id=group.id,  # type: ignore[arg-type]
    )


@router.get("/{group_id}", response_model=GroupResponse)
async def get_group(group_id: PositiveInt, session: AsyncSession = Depends(get_async_session)):
    service = GroupService()
    group = await service.get_by_id(session, group_id)

    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

    return group

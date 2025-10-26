from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.database.schemas.groups import GroupAddResponse, GroupCreateResponse, GroupResponse
from src.api.database.service.groups import GroupService
from src.database.connection import get_async_session

router = APIRouter(prefix="/groups", tags=["Groups"])


@router.get("/", response_model=list[GroupResponse])
async def list_groups(session: AsyncSession = Depends(get_async_session)):
    service = GroupService()
    return await service.get_all(session)


@router.post("/create", response_model=GroupCreateResponse)
async def create_group(name: str, session: AsyncSession = Depends(get_async_session)):
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


@router.post("/{group_id}/add-user", response_model=GroupAddResponse)
async def add_user(group_id: PositiveInt, user_id: UUID, session: AsyncSession = Depends(get_async_session)):
    service = GroupService()
    group, user, already_in_group = await service.add_user(session, group_id, user_id)

    if group is None or user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group or user not found")
    if already_in_group:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already in group")

    return GroupAddResponse(
        message="User successfully added to group",
        group_id=group.id,  # type: ignore[arg-type]
        user_id=user.id,
    )

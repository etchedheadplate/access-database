from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.access.services.remove import AccessRemoveService
from src.database.connection import get_async_session

router = APIRouter(prefix="/remove")


@router.delete("/user-from-group")
async def remove_user_from_group(
    user_id: UUID, group_id: PositiveInt, session: AsyncSession = Depends(get_async_session)
):
    service = AccessRemoveService()
    removed_user_from_group = await service.remove_user_from_group(session, user_id, group_id)
    return {"result": removed_user_from_group}


@router.delete("/permission-from-group")
async def remove_permission_from_group(
    permission_id: PositiveInt, group_id: PositiveInt, session: AsyncSession = Depends(get_async_session)
):
    service = AccessRemoveService()
    removed_permission_from_group = await service.remove_permission_from_group(session, permission_id, group_id)
    return {"result": removed_permission_from_group}


@router.delete("/resource-from-permission")
async def remove_resource_from_permission(
    resource_id: PositiveInt, permission_id: PositiveInt, session: AsyncSession = Depends(get_async_session)
):
    service = AccessRemoveService()
    removed_resource_from_permission = await service.remove_resource_from_permission(
        session, resource_id, permission_id
    )
    return {"result": removed_resource_from_permission}

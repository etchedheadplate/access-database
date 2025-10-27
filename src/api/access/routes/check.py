from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.access.services.check import AccessCheckService
from src.database.connection import get_async_session

router = APIRouter(prefix="/check")


@router.get("/user-in-group")
async def check_if_user_in_group(
    user_id: UUID, group_id: PositiveInt, session: AsyncSession = Depends(get_async_session)
) -> bool:
    service = AccessCheckService()
    user_in_group = await service.check_user_in_group(session, user_id, group_id)
    return {"result": user_in_group}  # type: ignore[arg-type]


@router.get("/permission-in-group")
async def check_if_permission_in_group(
    permission_id: PositiveInt, group_id: PositiveInt, session: AsyncSession = Depends(get_async_session)
) -> bool:
    service = AccessCheckService()
    permission_in_group = await service.check_permission_in_group(session, permission_id, group_id)
    return {"result": permission_in_group}  # type: ignore[arg-type]


@router.get("/resource-in-permission")
async def check_if_resource_in_permission(
    resource_id: PositiveInt, permission_id: PositiveInt, session: AsyncSession = Depends(get_async_session)
) -> bool:
    service = AccessCheckService()
    resource_in_permission = await service.check_resource_in_permission(session, resource_id, permission_id)
    return {"result": resource_in_permission}  # type: ignore[arg-type]

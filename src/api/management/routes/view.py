from fastapi import APIRouter, Depends
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.management.schemas.view import PermissionsViewResponse, ResourcesViewResponse, UserViewResponse
from src.api.management.services.view import AccessViewService
from src.database.connection import get_async_session

router = APIRouter(prefix="/view")


@router.get("/group-users", response_model=list[UserViewResponse])
async def view_group_users(group_id: PositiveInt, session: AsyncSession = Depends(get_async_session)):
    service = AccessViewService()
    return await service.view_group_users(session, group_id)


@router.get("/group-permissions", response_model=list[PermissionsViewResponse])
async def view_group_permissions(group_id: PositiveInt, session: AsyncSession = Depends(get_async_session)):
    service = AccessViewService()
    return await service.view_group_permissions(session, group_id)


@router.get("/permission-resources", response_model=list[ResourcesViewResponse])
async def view_permission_resources(permission_id: PositiveInt, session: AsyncSession = Depends(get_async_session)):
    service = AccessViewService()
    return await service.view_permission_resources(session, permission_id)

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.access.schemas.view import ViewPermissionsResponse, ViewResourcesResponse, ViewUserResponse
from src.api.access.services.view import AccessViewService
from src.database.connection import get_async_session

router = APIRouter(prefix="/view")


@router.get("/user-groups", response_model=list[ViewPermissionsResponse])
async def view_user_groups(
    user_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    service = AccessViewService()
    return await service.view_user_groups(session, user_id)


@router.get("/user-permissions", response_model=list[ViewPermissionsResponse])
async def view_user_permissions(
    user_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    service = AccessViewService()
    return await service.view_user_permissions(session, user_id)


@router.get("/user-resources", response_model=list[ViewResourcesResponse])
async def view_user_resources(user_id: UUID, session: AsyncSession = Depends(get_async_session)):
    service = AccessViewService()
    return await service.view_user_resources(session, user_id)


@router.get("/group-users", response_model=list[ViewUserResponse])
async def view_group_users(group_id: PositiveInt, session: AsyncSession = Depends(get_async_session)):
    service = AccessViewService()
    return await service.view_group_users(session, group_id)


@router.get("/group-permissions", response_model=list[ViewPermissionsResponse])
async def view_group_permissions(group_id: PositiveInt, session: AsyncSession = Depends(get_async_session)):
    service = AccessViewService()
    return await service.view_group_permissions(session, group_id)


@router.get("/group-resources", response_model=list[ViewResourcesResponse])
async def view_group_resources(group_id: PositiveInt, session: AsyncSession = Depends(get_async_session)):
    service = AccessViewService()
    return await service.view_group_resources(session, group_id)


@router.get("/permission-groups", response_model=list[ViewPermissionsResponse])
async def view_permission_groups(
    permission_id: PositiveInt,
    session: AsyncSession = Depends(get_async_session),
):
    service = AccessViewService()
    return await service.view_permission_groups(session, permission_id)


@router.get("/permission-users", response_model=list[ViewUserResponse])
async def view_permission_users(permission_id: PositiveInt, session: AsyncSession = Depends(get_async_session)):
    service = AccessViewService()
    return await service.view_permission_users(session, permission_id)


@router.get("/permission-resources", response_model=list[ViewResourcesResponse])
async def view_permission_resources(permission_id: PositiveInt, session: AsyncSession = Depends(get_async_session)):
    service = AccessViewService()
    return await service.view_permission_resources(session, permission_id)


@router.get("/resource-permissions", response_model=list[ViewPermissionsResponse])
async def view_resource_permissions(resource_id: PositiveInt, session: AsyncSession = Depends(get_async_session)):
    service = AccessViewService()
    return await service.view_resource_permissions(session, resource_id)


@router.get("/resource-groups", response_model=list[ViewPermissionsResponse])
async def view_resource_groups(resource_id: PositiveInt, session: AsyncSession = Depends(get_async_session)):
    service = AccessViewService()
    return await service.view_resource_groups(session, resource_id)


@router.get("/resource-users", response_model=list[ViewUserResponse])
async def view_resource_users(resource_id: PositiveInt, session: AsyncSession = Depends(get_async_session)):
    service = AccessViewService()
    return await service.view_resource_users(session, resource_id)

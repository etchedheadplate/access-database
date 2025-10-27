from fastapi import APIRouter, Depends
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.access.schemas.view import PermissionsViewResponse, ResourcesViewResponse, UserViewResponse
from src.api.access.services.view import AccessViewService
from src.auth.manager import current_active_user
from src.database.connection import get_async_session
from src.database.models import User

router = APIRouter(prefix="/view")


@router.get("/group-users", response_model=list[UserViewResponse])
async def view_group_users(
    group_id: PositiveInt, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_active_user)
):
    service = AccessViewService()
    return await service.view_group_users(session, group_id)


@router.get("/group-permissions", response_model=list[PermissionsViewResponse])
async def view_group_permissions(
    group_id: PositiveInt, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_active_user)
):
    service = AccessViewService()
    return await service.view_group_permissions(session, group_id)


@router.get("/permission-resources", response_model=list[ResourcesViewResponse])
async def view_permission_resources(
    permission_id: PositiveInt,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    service = AccessViewService()
    return await service.view_permission_resources(session, permission_id)

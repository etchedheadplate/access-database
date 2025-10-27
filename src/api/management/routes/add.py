from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.management.schemas.add import PermissionGrantResponse, ResourceLinkResponse, UserAddResponse
from src.api.management.services.add import AccessGrantService
from src.database.connection import get_async_session

router = APIRouter(prefix="/add", tags=["Management"])


@router.post("/user-to-group", response_model=UserAddResponse)
async def add_user_to_group(user_id: UUID, group_id: PositiveInt, session: AsyncSession = Depends(get_async_session)):
    service = AccessGrantService()
    group, user, already_added = await service.add_user_to_group(session, group_id, user_id)

    if group is None or user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group or user not found")
    if already_added:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already in group")

    return UserAddResponse(
        message="User successfully added to group",
        user_id=user.id,
        user_email=user.email,
        group_id=group.id,
        group_name=group.name,
    )


@router.post("/permission-to-group", response_model=PermissionGrantResponse)
async def add_permission_to_group(
    permission_id: PositiveInt, group_id: PositiveInt, session: AsyncSession = Depends(get_async_session)
):
    service = AccessGrantService()
    permission, group, already_added = await service.add_permission_to_group(session, permission_id, group_id)

    if permission is None or group is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission or group not found")
    if already_added:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Permission already added to group")

    return PermissionGrantResponse(
        message="Permission successfully added to group",
        permission_id=permission.id,
        permission_name=permission.name,
        group_id=group.id,
        group_name=group.name,
    )


@router.post("/resource-to-permission", response_model=ResourceLinkResponse)
async def add_resource_to_permission(
    resource_id: PositiveInt, permission_id: PositiveInt, session: AsyncSession = Depends(get_async_session)
):
    service = AccessGrantService()
    resource, permission, already_added = await service.add_resource_to_permission(session, resource_id, permission_id)

    if resource is None or permission is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource or permission not found")
    if already_added:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resource already added to permission")

    return ResourceLinkResponse(
        message="Resource successfully added to permission",
        resource_id=resource.id,
        resource_name=resource.name,
        permission_id=permission.id,
        permission_name=permission.name,
    )

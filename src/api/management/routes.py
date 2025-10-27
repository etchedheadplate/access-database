from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.management.schemas import PermissionGrantResponse, ResourceLinkResponse, UserAddResponse
from src.api.management.services import AccessGrantService
from src.database.connection import get_async_session

router = APIRouter(tags=["Management"])


@router.post("/add-user", response_model=UserAddResponse)
async def add_user_to_group(user_id: UUID, group_id: PositiveInt, session: AsyncSession = Depends(get_async_session)):
    service = AccessGrantService()
    group, user, already_in_group = await service.add_user_to_group(session, group_id, user_id)

    if group is None or user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group or user not found")
    if already_in_group:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already in group")

    return UserAddResponse(
        message="User successfully added to group",
        user_id=user.id,
        group_id=group.id,  # type: ignore[arg-type]
    )


@router.post("/grant-permission", response_model=PermissionGrantResponse)
async def grant_permission_to_group(
    permission_id: PositiveInt, group_id: PositiveInt, session: AsyncSession = Depends(get_async_session)
):
    service = AccessGrantService()
    permission, group, already_granted = await service.grant_permission_to_group(session, permission_id, group_id)

    if permission is None or group is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission or group not found")
    if already_granted:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Permission already granted to group")

    return PermissionGrantResponse(message="Permission successfully linked to group", permission_id=permission.id, group_id=group.id)  # type: ignore[arg-type]


@router.post("/link-resource", response_model=ResourceLinkResponse)
async def link_resource_to_permission(
    resource_id: PositiveInt, permission_id: PositiveInt, session: AsyncSession = Depends(get_async_session)
):
    service = AccessGrantService()
    resource, permission, already_linked = await service.link_resource_to_permission(
        session, resource_id, permission_id
    )

    if resource is None or permission is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource or permission not found")
    if already_linked:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resource already linked to permission")

    return ResourceLinkResponse(
        message="Resource successfully linked to permission", resource_id=resource.id, permission_id=permission.id  # type: ignore[arg-type]
    )

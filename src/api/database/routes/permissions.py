from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.database.schemas.permissions import PermissionCreateResponse, PermissionLinkResponse, PermissionResponse
from src.api.database.service.permissions import PermissionService
from src.database.connection import get_async_session

router = APIRouter(prefix="/permissions", tags=["Permissions"])


@router.get("/", response_model=list[PermissionResponse])
async def list_permissions(session: AsyncSession = Depends(get_async_session)):
    service = PermissionService()
    return await service.get_all(session)


@router.post("/create", response_model=PermissionCreateResponse)
async def create_permission(name: str, session: AsyncSession = Depends(get_async_session)):
    service = PermissionService()
    permission = await service.create(session, name)

    if not permission:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Permission with this name already exists")

    return PermissionCreateResponse(
        message="Permission successfully created",
        id=permission.id,  # type: ignore[arg-type]
    )


@router.get("/{permission_id}", response_model=PermissionResponse)
async def get_permission(permission_id: PositiveInt, session: AsyncSession = Depends(get_async_session)):
    service = PermissionService()
    permission = await service.get_by_id(session, permission_id)

    if not permission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")

    return permission


@router.post("/{permission_id}/link-group", response_model=PermissionLinkResponse)
async def link_group(
    permission_id: PositiveInt, group_id: PositiveInt, session: AsyncSession = Depends(get_async_session)
):
    service = PermissionService()
    permission, group, already_linked = await service.link_to_group(session, permission_id, group_id)

    if permission is None or group is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission or group not found")
    if already_linked:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Permission already linked to group")

    return PermissionLinkResponse(message="Permission successfully linked to group", permission_id=permission.id, group_id=group.id)  # type: ignore[arg-type]

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.database.schemas.permissions import PermissionCreateResponse, PermissionResponse
from src.api.database.services.permissions import PermissionService
from src.auth.manager import current_active_user
from src.database.connection import get_async_session
from src.database.models import User

router = APIRouter(prefix="/permissions")


@router.get("/", response_model=list[PermissionResponse])
async def list_permissions(session: AsyncSession = Depends(get_async_session)):
    service = PermissionService()
    return await service.get_all(session)


@router.post("/create", response_model=PermissionCreateResponse)
async def create_permission(
    name: str, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_active_user)
):
    service = PermissionService()
    permission = await service.create(session, name)

    if not permission:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Permission with this name already exists")

    return PermissionCreateResponse(
        message="Permission successfully created",
        id=permission.id,
    )


@router.get("/{permission_id}", response_model=PermissionResponse)
async def get_permission(permission_id: PositiveInt, session: AsyncSession = Depends(get_async_session)):
    service = PermissionService()
    permission = await service.get_by_id(session, permission_id)

    if not permission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")

    return permission

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.database.schemas.accesses import AccessCreateResponse, AccessLinkResponse, AccessResponse
from src.api.database.service.accesses import AccessService
from src.database.connection import get_async_session

router = APIRouter(prefix="/accesses", tags=["Accesses"])


@router.get("/", response_model=list[AccessResponse])
async def list_accesses(session: AsyncSession = Depends(get_async_session)):
    service = AccessService()
    return await service.get_all(session)


@router.post("/create", response_model=AccessCreateResponse)
async def create_access(name: str, session: AsyncSession = Depends(get_async_session)):
    service = AccessService()
    access = await service.create(session, name)

    if not access:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Access with this name already exists")

    return AccessCreateResponse(
        message="Access successfully created",
        id=access.id,  # type: ignore[arg-type]
    )


@router.get("/{access_id}", response_model=AccessResponse)
async def get_access(access_id: PositiveInt, session: AsyncSession = Depends(get_async_session)):
    service = AccessService()
    access = await service.get_by_id(session, access_id)

    if not access:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Access not found")

    return access


@router.post("/{access_id}/link-group", response_model=AccessLinkResponse)
async def link_group(access_id: PositiveInt, group_id: PositiveInt, session: AsyncSession = Depends(get_async_session)):
    service = AccessService()
    access, group, already_linked = await service.link_to_group(session, access_id, group_id)

    if access is None or group is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Access or group not found")
    if already_linked:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Access already linked to group")

    return AccessLinkResponse(message="Access successfully linked to group", access_id=access.id, group_id=group.id)  # type: ignore[arg-type]

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.database.schemas.resources import ResourceCreateResponse, ResourceLinkResponse, ResourceResponse
from src.api.database.services.resources import ResourceService
from src.database.connection import get_async_session

router = APIRouter(prefix="/resources", tags=["Resources"])


@router.get("/", response_model=list[ResourceResponse])
async def list_resources(session: AsyncSession = Depends(get_async_session)):
    service = ResourceService()
    return await service.get_all(session)


@router.post("/create", response_model=ResourceCreateResponse)
async def create_resource(name: str, session: AsyncSession = Depends(get_async_session)):
    service = ResourceService()
    resource = await service.create(session, name)

    if not resource:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resource with this name already exists")

    return ResourceCreateResponse(
        message="Resource successfully created",
        id=resource.id,  # type: ignore[arg-type]
    )


@router.get("/{resource_id}", response_model=ResourceResponse)
async def get_resource(resource_id: PositiveInt, session: AsyncSession = Depends(get_async_session)):
    service = ResourceService()
    resource = await service.get_by_id(session, resource_id)

    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

    return resource


@router.post("/{resource_id}/link-permission", response_model=ResourceLinkResponse)
async def link_permission(
    resource_id: PositiveInt, permission_id: PositiveInt, session: AsyncSession = Depends(get_async_session)
):
    service = ResourceService()
    resource, permission, already_linked = await service.link_to_permission(session, resource_id, permission_id)

    if resource is None or permission is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource or permission not found")
    if already_linked:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resource already linked to permission")

    return ResourceLinkResponse(
        message="Resource successfully linked to permission", resource_id=resource.id, permission_id=permission.id  # type: ignore[arg-type]
    )

from uuid import UUID

from pydantic import BaseModel, PositiveInt


class UserAddResponse(BaseModel):
    message: str
    user_id: UUID
    group_id: PositiveInt


class PermissionGrantResponse(BaseModel):
    message: str
    asset_id: PositiveInt
    group_id: PositiveInt


class ResourceLinkResponse(BaseModel):
    message: str
    resource_id: PositiveInt
    permission_id: PositiveInt

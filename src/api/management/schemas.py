from uuid import UUID

from pydantic import BaseModel, EmailStr, PositiveInt


class UserAddResponse(BaseModel):
    message: str
    user_id: UUID
    user_email: EmailStr
    group_id: PositiveInt
    group_name: str


class PermissionGrantResponse(BaseModel):
    message: str
    permission_id: PositiveInt
    permission_name: str
    group_id: PositiveInt
    group_name: str


class ResourceLinkResponse(BaseModel):
    message: str
    resource_id: PositiveInt
    resource_name: str
    permission_id: PositiveInt
    permission_name: str

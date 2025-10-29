from uuid import UUID

from pydantic import BaseModel, EmailStr, PositiveInt


class AddUserResponse(BaseModel):
    message: str
    user_id: UUID
    user_email: EmailStr
    group_id: PositiveInt
    group_name: str


class AddPermissionResponse(BaseModel):
    message: str
    permission_id: PositiveInt
    permission_name: str
    group_id: PositiveInt
    group_name: str


class AddResourceResponse(BaseModel):
    message: str
    resource_id: PositiveInt
    resource_name: str
    permission_id: PositiveInt
    permission_name: str

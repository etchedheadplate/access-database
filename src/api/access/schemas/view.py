from uuid import UUID

from pydantic import BaseModel, EmailStr, PositiveInt


class UserViewResponse(BaseModel):
    id: UUID
    email: EmailStr

    class Config:
        from_attributes = True


class PermissionsViewResponse(BaseModel):
    id: PositiveInt
    name: str


class ResourcesViewResponse(BaseModel):
    id: PositiveInt
    name: str

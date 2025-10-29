from uuid import UUID

from pydantic import BaseModel, EmailStr, PositiveInt


class ViewUserResponse(BaseModel):
    id: UUID
    email: EmailStr

    class Config:
        from_attributes = True


class ViewPermissionsResponse(BaseModel):
    id: PositiveInt
    name: str


class ViewResourcesResponse(BaseModel):
    id: PositiveInt
    name: str

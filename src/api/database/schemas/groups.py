from uuid import UUID

from pydantic import BaseModel, PositiveInt


class GroupResponse(BaseModel):
    id: PositiveInt
    name: str

    class Config:
        from_attributes = True


class GroupCreateResponse(BaseModel):
    message: str
    id: PositiveInt


class GroupAddResponse(BaseModel):
    message: str
    group_id: PositiveInt
    user_id: UUID

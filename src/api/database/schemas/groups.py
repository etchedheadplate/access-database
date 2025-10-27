from pydantic import BaseModel, PositiveInt


class GroupResponse(BaseModel):
    id: PositiveInt
    name: str

    class Config:
        from_attributes = True


class GroupCreateResponse(BaseModel):
    message: str
    id: PositiveInt

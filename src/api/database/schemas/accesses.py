from pydantic import BaseModel, PositiveInt


class AccessResponse(BaseModel):
    id: PositiveInt
    name: str

    class Config:
        from_attributes = True


class AccessCreateResponse(BaseModel):
    message: str
    id: PositiveInt


class AccessLinkResponse(BaseModel):
    message: str
    access_id: PositiveInt
    group_id: PositiveInt

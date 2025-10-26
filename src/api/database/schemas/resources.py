from pydantic import BaseModel, PositiveInt


class ResourceResponse(BaseModel):
    id: PositiveInt
    name: str

    class Config:
        from_attributes = True


class ResourceCreateResponse(BaseModel):
    message: str
    id: PositiveInt


class ResourceLinkResponse(BaseModel):
    message: str
    resource_id: PositiveInt
    access_id: PositiveInt

from pydantic import BaseModel, PositiveInt


class PermissionResponse(BaseModel):
    id: PositiveInt
    name: str

    class Config:
        from_attributes = True


class PermissionCreateResponse(BaseModel):
    message: str
    id: PositiveInt


class PermissionLinkResponse(BaseModel):
    message: str
    asset_id: PositiveInt
    group_id: PositiveInt

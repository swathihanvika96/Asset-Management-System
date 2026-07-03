from datetime import date
from pydantic import BaseModel


class AssetBase(BaseModel):
    asset_name: str
    asset_type: str
    asset_tag: str
    purchase_date: date
    status: str


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    asset_name: str
    asset_type: str
    asset_tag: str
    purchase_date: date
    status: str


class AssetResponse(AssetBase):
    id: int
    is_deleted: bool

    class Config:
        from_attributes = True
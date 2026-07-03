from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import (
    admin_required,
    get_current_user
)

from app.schemas.asset import (
    AssetCreate,
    AssetUpdate
)

from app.services.asset_service import AssetService

router = APIRouter(
    prefix="/assets",
    tags=["Assets"]
)


@router.post("/")
def create_asset(
    asset: AssetCreate,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):
    return AssetService.create_asset(
        db,
        asset
    )


@router.get("/")
def get_assets(
    page: int = 1,
    limit: int = 10,
    search: str = None,
    status: str = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return AssetService.get_assets(
        db,
        page,
        limit,
        search,
        status
    )


@router.get("/{asset_id}")
def get_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return AssetService.get_asset(
        db,
        asset_id
    )


@router.put("/{asset_id}")
def update_asset(
    asset_id: int,
    asset: AssetUpdate,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):
    return AssetService.update_asset(
        db,
        asset_id,
        asset
    )


@router.delete("/{asset_id}")
def delete_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):
    return AssetService.delete_asset(
        db,
        asset_id
    )
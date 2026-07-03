from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetUpdate


class AssetService:

    @staticmethod
    def create_asset(db: Session, asset: AssetCreate):

        existing = db.query(Asset).filter(
            Asset.asset_tag == asset.asset_tag,
            Asset.is_deleted == False
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Asset tag already exists."
            )

        new_asset = Asset(
            asset_name=asset.asset_name,
            asset_type=asset.asset_type,
            asset_tag=asset.asset_tag,
            purchase_date=asset.purchase_date,
            status=asset.status
        )

        db.add(new_asset)
        db.commit()
        db.refresh(new_asset)

        return new_asset

    @staticmethod
    def get_assets(
        db: Session,
        page: int = 1,
        limit: int = 10,
        search: str = None,
        status_filter: str = None
    ):

        query = db.query(Asset).filter(
            Asset.is_deleted == False
        )

        if search:
            query = query.filter(
                or_(
                    Asset.asset_name.ilike(f"%{search}%"),
                    Asset.asset_tag.ilike(f"%{search}%")
                )
            )

        if status_filter:
            query = query.filter(
                Asset.status == status_filter
            )

        total = query.count()

        assets = query.offset(
            (page - 1) * limit
        ).limit(limit).all()

        return {
            "total": total,
            "page": page,
            "limit": limit,
            "data": assets
        }

    @staticmethod
    def get_asset(db: Session, asset_id: int):

        asset = db.query(Asset).filter(
            Asset.id == asset_id,
            Asset.is_deleted == False
        ).first()

        if not asset:
            raise HTTPException(
                status_code=404,
                detail="Asset not found."
            )

        return asset

    @staticmethod
    def update_asset(
        db: Session,
        asset_id: int,
        asset_data: AssetUpdate
    ):

        asset = db.query(Asset).filter(
            Asset.id == asset_id,
            Asset.is_deleted == False
        ).first()

        if not asset:
            raise HTTPException(
                status_code=404,
                detail="Asset not found."
            )

        duplicate = db.query(Asset).filter(
            Asset.asset_tag == asset_data.asset_tag,
            Asset.id != asset_id,
            Asset.is_deleted == False
        ).first()

        if duplicate:
            raise HTTPException(
                status_code=400,
                detail="Asset tag already exists."
            )

        asset.asset_name = asset_data.asset_name
        asset.asset_type = asset_data.asset_type
        asset.asset_tag = asset_data.asset_tag
        asset.purchase_date = asset_data.purchase_date
        asset.status = asset_data.status

        db.commit()
        db.refresh(asset)

        return asset

    @staticmethod
    def delete_asset(db: Session, asset_id: int):

        asset = db.query(Asset).filter(
            Asset.id == asset_id,
            Asset.is_deleted == False
        ).first()

        if not asset:
            raise HTTPException(
                status_code=404,
                detail="Asset not found."
            )

        asset.is_deleted = True

        db.commit()

        return {
            "message": "Asset deleted successfully."
        }
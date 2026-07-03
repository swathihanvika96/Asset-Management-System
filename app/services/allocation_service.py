from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.models.user import User
from app.models.allocation import Allocation
from app.schemas.allocation import AllocationCreate, AllocationUpdate


class AllocationService:

    @staticmethod
    def allocate_asset(db: Session, allocation: AllocationCreate):

        # Check Asset
        asset = db.query(Asset).filter(
            Asset.id == allocation.asset_id,
            Asset.is_deleted == False
        ).first()

        if not asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asset not found."
            )

        # Asset should be available
        if asset.status != "Available":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Asset is not available for allocation."
            )

        # Check Employee
        employee = db.query(User).filter(
            User.id == allocation.employee_id,
            User.role == "Employee",
            User.is_active == True
        ).first()

        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found."
            )

        # Prevent duplicate active allocation
        active_allocation = db.query(Allocation).filter(
            Allocation.asset_id == allocation.asset_id,
            Allocation.allocation_status == "Assigned"
        ).first()

        if active_allocation:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Asset is already assigned."
            )

        new_allocation = Allocation(
            asset_id=allocation.asset_id,
            employee_id=allocation.employee_id,
            assigned_date=allocation.assigned_date,
            allocation_status="Assigned"
        )

        db.add(new_allocation)

        # Update asset status
        asset.status = "Assigned"

        db.commit()
        db.refresh(new_allocation)

        return {
            "message": "Asset allocated successfully.",
            "data": new_allocation
        }

    @staticmethod
    def get_allocations(db: Session):

        allocations = db.query(Allocation).all()

        return allocations

    @staticmethod
    def get_allocation(db: Session, allocation_id: int):

        allocation = db.query(Allocation).filter(
            Allocation.id == allocation_id
        ).first()

        if not allocation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Allocation not found."
            )

        return allocation

    @staticmethod
    def update_allocation(
        db: Session,
        allocation_id: int,
        allocation_data: AllocationUpdate
    ):

        allocation = db.query(Allocation).filter(
            Allocation.id == allocation_id
        ).first()

        if not allocation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Allocation not found."
            )

        if allocation.allocation_status == "Returned":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Asset already returned."
            )

        asset = db.query(Asset).filter(
            Asset.id == allocation.asset_id
        ).first()

        allocation.return_date = allocation_data.return_date
        allocation.allocation_status = allocation_data.allocation_status

        if allocation_data.allocation_status == "Returned":
            asset.status = "Available"

        elif allocation_data.allocation_status == "Lost":
            asset.status = "Lost"

        db.commit()
        db.refresh(allocation)

        return {
            "message": "Allocation updated successfully.",
            "data": allocation
        }

    @staticmethod
    def employee_assets(
        db: Session,
        employee_id: int
    ):

        allocations = db.query(Allocation).filter(
            Allocation.employee_id == employee_id,
            Allocation.allocation_status == "Assigned"
        ).all()

        result = []

        for allocation in allocations:

            asset = db.query(Asset).filter(
                Asset.id == allocation.asset_id
            ).first()

            if asset:
                result.append({
                    "allocation_id": allocation.id,
                    "asset_id": asset.id,
                    "asset_name": asset.asset_name,
                    "asset_type": asset.asset_type,
                    "asset_tag": asset.asset_tag,
                    "assigned_date": allocation.assigned_date,
                    "status": allocation.allocation_status
                })

        return result
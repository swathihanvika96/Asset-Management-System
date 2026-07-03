from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import admin_required, get_current_user

from app.schemas.allocation import (
    AllocationCreate,
    AllocationUpdate
)

from app.services.allocation_service import AllocationService

router = APIRouter(
    prefix="/allocations",
    tags=["Allocations"]
)


@router.post("/")
def allocate_asset(
    allocation: AllocationCreate,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):
    return AllocationService.allocate_asset(
        db,
        allocation
    )


@router.get("/")
def get_allocations(
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):
    return AllocationService.get_allocations(db)


@router.get("/{allocation_id}")
def get_allocation(
    allocation_id: int,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):
    return AllocationService.get_allocation(
        db,
        allocation_id
    )


@router.put("/{allocation_id}")
def return_asset(
    allocation_id: int,
    allocation: AllocationUpdate,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):
    return AllocationService.return_asset(
        db,
        allocation_id,
        allocation
    )


@router.get("/employee/{employee_id}")
def employee_assets(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Admin -> can view any employee's assets

    Employee -> can only view their own assets
    """

    if current_user.role == "Employee":
        if current_user.id != employee_id:
            return {
                "message": "You can view only your assets."
            }

    return AllocationService.employee_assets(
        db,
        employee_id
    )
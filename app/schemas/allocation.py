from datetime import date
from typing import Optional
from pydantic import BaseModel


class AllocationBase(BaseModel):
    asset_id: int
    employee_id: int
    assigned_date: date
    allocation_status: str


class AllocationCreate(AllocationBase):
    pass


class AllocationUpdate(BaseModel):
    return_date: Optional[date] = None
    allocation_status: str


class AllocationResponse(AllocationBase):
    id: int
    return_date: Optional[date]

    class Config:
        from_attributes = True
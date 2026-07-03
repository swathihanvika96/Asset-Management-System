from sqlalchemy import Column, Integer, Date, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Allocation(Base):
    __tablename__ = "allocations"

    id = Column(Integer, primary_key=True, index=True)

    asset_id = Column(
        Integer,
        ForeignKey("assets.id"),
        nullable=False
    )

    employee_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    assigned_date = Column(Date, nullable=False)

    return_date = Column(Date, nullable=True)

    allocation_status = Column(
        String(20),
        default="Assigned"
    )

    asset = relationship(
        "Asset",
        back_populates="allocations"
    )

    employee = relationship(
        "User",
        back_populates="allocations"
    )
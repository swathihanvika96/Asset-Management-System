from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import relationship

from app.core.database import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)

    asset_name = Column(String(100), nullable=False)

    asset_type = Column(String(100), nullable=False)

    asset_tag = Column(String(100), unique=True, nullable=False)

    purchase_date = Column(Date, nullable=False)

    status = Column(String(30), default="Available")

    is_deleted = Column(Boolean, default=False)

    allocations = relationship(
        "Allocation",
        back_populates="asset",
        cascade="all, delete-orphan"
    )
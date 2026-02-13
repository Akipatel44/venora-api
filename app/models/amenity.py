from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, func
from sqlalchemy.orm import relationship
from app.database import Base


class Amenity(Base):
    __tablename__ = "amenities"

    amenity_id = Column(Integer, primary_key=True, index=True)
    amenity_name = Column(String(255), nullable=False, unique=True)
    is_chargeable = Column(Boolean, nullable=False, default=False)
    base_price = Column(Numeric(10, 2), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    halls = relationship("HallAmenity", back_populates="amenity")

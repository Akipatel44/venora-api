from sqlalchemy import Column, Integer, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class HallAmenity(Base):
    __tablename__ = "hall_amenities"

    id = Column(Integer, primary_key=True, index=True)
    hall_id = Column(Integer, ForeignKey("halls.hall_id"), nullable=False, index=True)
    amenity_id = Column(Integer, ForeignKey("amenities.amenity_id"), nullable=False, index=True)
    custom_price = Column(Numeric(10, 2), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    hall = relationship("Hall", back_populates="amenities")
    amenity = relationship("Amenity", back_populates="halls")

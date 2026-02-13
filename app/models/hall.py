from sqlalchemy import Column, Integer, String, DateTime, Numeric, Text, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


class Hall(Base):
    __tablename__ = "halls"

    hall_id = Column(Integer, primary_key=True, index=True)
    subadmin_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    hall_name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    capacity = Column(Integer, nullable=False)
    base_price = Column(Numeric(10, 2), nullable=False)
    commission_percent = Column(Numeric(5, 2), nullable=True)
    status = Column(String(50), nullable=False, default="pending")
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    subadmin = relationship("User", foreign_keys=[subadmin_id])
    amenities = relationship("HallAmenity", back_populates="hall")
    services = relationship("HallService", back_populates="hall")

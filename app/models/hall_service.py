from sqlalchemy import Column, Integer, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class HallService(Base):
    __tablename__ = "hall_services"

    id = Column(Integer, primary_key=True, index=True)
    hall_id = Column(Integer, ForeignKey("halls.hall_id"), nullable=False, index=True)
    service_id = Column(Integer, ForeignKey("services.service_id"), nullable=False, index=True)
    custom_price = Column(Numeric(10, 2), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    hall = relationship("Hall", back_populates="services")
    service = relationship("Service", back_populates="halls")

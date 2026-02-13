from sqlalchemy import Column, Integer, String, DateTime, Numeric, func
from sqlalchemy.orm import relationship
from app.database import Base


class Service(Base):
    __tablename__ = "services"

    service_id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String(255), nullable=False)
    service_type = Column(String(50), nullable=False)
    base_price = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    halls = relationship("HallService", back_populates="service")

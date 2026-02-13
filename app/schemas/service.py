from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from decimal import Decimal


class ServiceCreate(BaseModel):
    service_name: str
    service_type: str
    base_price: Decimal

    @field_validator("base_price")
    @classmethod
    def base_price_positive(cls, v):
        if v <= 0:
            raise ValueError("base_price must be greater than 0")
        return v


class ServiceResponse(BaseModel):
    service_id: int
    service_name: str
    service_type: str
    base_price: Decimal
    created_at: datetime

    class Config:
        orm_mode = True


class HallServiceCreate(BaseModel):
    hall_id: int
    service_id: int
    custom_price: Optional[Decimal] = None
    is_active: bool = True

    @field_validator("custom_price")
    @classmethod
    def custom_price_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("custom_price must be greater than 0")
        return v


class HallServiceResponse(BaseModel):
    id: int
    hall_id: int
    service_id: int
    custom_price: Optional[Decimal] = None
    is_active: bool

    class Config:
        orm_mode = True

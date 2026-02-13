from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from decimal import Decimal


class HallCreate(BaseModel):
    hall_name: str
    location: str
    capacity: int
    base_price: Decimal
    commission_percent: Optional[Decimal] = None
    description: Optional[str] = None
    subadmin_id: int

    @field_validator("capacity")
    @classmethod
    def capacity_positive(cls, v):
        if v <= 0:
            raise ValueError("capacity must be greater than 0")
        return v

    @field_validator("base_price")
    @classmethod
    def base_price_positive(cls, v):
        if v <= 0:
            raise ValueError("base_price must be greater than 0")
        return v


class HallUpdate(BaseModel):
    hall_name: Optional[str] = None
    location: Optional[str] = None
    capacity: Optional[int] = None
    base_price: Optional[Decimal] = None
    commission_percent: Optional[Decimal] = None
    status: Optional[str] = None
    description: Optional[str] = None

    @field_validator("capacity")
    @classmethod
    def capacity_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("capacity must be greater than 0")
        return v

    @field_validator("base_price")
    @classmethod
    def base_price_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("base_price must be greater than 0")
        return v


class HallResponse(BaseModel):
    hall_id: int
    hall_name: str
    location: str
    capacity: int
    base_price: Decimal
    commission_percent: Optional[Decimal] = None
    status: str
    subadmin_id: int
    description: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True

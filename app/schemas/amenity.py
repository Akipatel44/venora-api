from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from decimal import Decimal


class AmenityCreate(BaseModel):
    amenity_name: str
    is_chargeable: bool = False
    base_price: Optional[Decimal] = None

    @field_validator("base_price")
    @classmethod
    def base_price_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("base_price must be greater than 0")
        return v


class AmenityResponse(BaseModel):
    amenity_id: int
    amenity_name: str
    is_chargeable: bool
    base_price: Optional[Decimal] = None
    created_at: datetime

    class Config:
        orm_mode = True


class HallAmenityCreate(BaseModel):
    hall_id: int
    amenity_id: int
    custom_price: Optional[Decimal] = None
    is_active: bool = True

    @field_validator("custom_price")
    @classmethod
    def custom_price_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("custom_price must be greater than 0")
        return v


class HallAmenityResponse(BaseModel):
    id: int
    hall_id: int
    amenity_id: int
    custom_price: Optional[Decimal] = None
    is_active: bool

    class Config:
        orm_mode = True

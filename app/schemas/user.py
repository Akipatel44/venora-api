from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    full_name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role: Optional[str] = "customer"


class UserOut(UserBase):
    user_id: int
    role: str
    status: str
    created_at: datetime

    class Config:
        orm_mode = True

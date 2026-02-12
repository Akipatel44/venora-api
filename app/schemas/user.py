from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    full_name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role: Optional[str] = "customer"


class TokenOut(BaseModel):
    access_token: str
    token_type: str
    role: str


class UserOut(UserBase):
    user_id: int
    role: str
    status: str
    created_at: datetime

    class Config:
        orm_mode = True

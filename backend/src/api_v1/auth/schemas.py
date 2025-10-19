from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict, Field

from src.models.user import UserRole
from typing import Optional

class RegisterSchema(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name:str = Field(..., min_length=2, max_length=50)
    email: EmailStr = Field(..., min_length=5, max_length=50)
    password: str = Field(..., min_length=8, max_length=50)
    role: Optional[UserRole] = Field(...)
    model_config = ConfigDict(from_attributes=True)


class LoginSchema(BaseModel):
    email: EmailStr = Field(..., min_length=5, max_length=50)
    password: str = Field(..., min_length=8, max_length=50)

    model_config = ConfigDict(from_attributes=True)


class TokenSchema(BaseModel):
    refresh: str
    access: str


class UserPayloadSchema(BaseModel):
    user_id: int
    role: UserRole

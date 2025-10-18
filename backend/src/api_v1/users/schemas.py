from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from src.models.user import UserRole


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name:str
    role: UserRole
    model_config = ConfigDict(from_attributes=True)


class UserUpdateSchema(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] =None
    password: Optional[str] = None
    role: Optional[UserRole] = None

    model_config = ConfigDict(from_attributes=True)


class UserDTO(UserCreateSchema):
    pass


class UserModelSchema(UserCreateSchema):
    id: int
    created_at: datetime
    updated_at: datetime

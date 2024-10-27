from pydantic import BaseModel, PositiveFloat, EmailStr, validator, Field
from enum import Enum
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    user_id: int
    user_name: str
    user_email: EmailStr
    content: str
    created_at: datetime

class PostCreate(BaseModel):
    content: str

class PostUpdate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
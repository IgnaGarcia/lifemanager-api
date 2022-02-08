from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"

class UserBase(BaseModel):
    uuid: Optional[str]
    name: str
    email: EmailStr
    age: int
    role: Role
    class Config:
        orm_mode = True
    
class User(UserBase):
    password: str
    
class UserUpdateReq(BaseModel):
    name: Optional[str]
    password: Optional[str]
    age: Optional[int]
    role: Optional[Role]
    
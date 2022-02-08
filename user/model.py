from pydantic import BaseModel
from typing import Optional
from enum import Enum

class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"

class User(BaseModel):
    uuid: Optional[str]
    name: str
    age: int
    role: Role
    class Config:
        orm_mode = True
    
class UserUpdateReq(BaseModel):
    name: Optional[str]
    age: Optional[int]
    role: Optional[Role]
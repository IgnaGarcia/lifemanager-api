from pydantic import BaseModel, EmailStr

class LoginReq(BaseModel):
    email: EmailStr
    password: str
    
    class Config:
        orm_mode = True
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from user.model import Role

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*6
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    uuid: str
    role: str


def generate_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)
    
    return encoded_jwt



credentials_exception = HTTPException(
    status_code= 401,
    detail= "Could not validate credentials",
    headers= {"WWW-Authenticate": "Bearer"},
)
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uuid: str = payload.get("uuid")
        role: str = payload.get("role")
        
        if not uuid or not role:
            raise credentials_exception
        return TokenData(uuid= uuid, role= role)
    except JWTError:
        raise credentials_exception


async def current_user(token: str = Depends(oauth2_scheme)):
    return verify_token(token)
    #user = get_user(fake_users_db, username=token_data.username)
    #return user
    
async def current_admin(token: str = Depends(oauth2_scheme)):
    data = verify_token(token)
    if data.role != Role.ADMIN:
        raise credentials_exception
    return data
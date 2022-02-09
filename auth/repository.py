from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from database.schemas import Users
from auth.token import generate_token, Token
from user.model import UserBase
from util.hash import Hash

def login(req: OAuth2PasswordRequestForm, db: Session):
    user = db.query(Users).filter(Users.email == req.username).first()
    if not user or not Hash.verify(req.password, user.password):
        raise HTTPException(status_code= 401, detail= 'Invalid credentials')

    access_token = generate_token({"uuid": user.uuid, "role": user.role})
    return Token(access_token= access_token, token_type= "bearer")
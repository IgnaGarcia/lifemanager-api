from fastapi import HTTPException
from sqlalchemy.orm import Session
from database.schemas import Users
from auth.model import LoginReq
from auth.token import generate_token
from user.model import UserBase
from util.hash import Hash

def login(req: LoginReq, db: Session):
    user = db.query(Users).filter(Users.email == req.email).first()
    if not user or not Hash.verify(req.password, user.password):
        raise HTTPException(status_code= 401, detail= 'Invalid credentials')

    access_token = generate_token({"uuid": user.uuid, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}
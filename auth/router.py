from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.model import LoginReq
from auth.token import Token
from database.db import get_db
from auth import repository

auth = APIRouter()        


@auth.post('/login', summary="Get access token with user credentials",
            status_code=200, response_model=Token,
            responses={
                200: {
                    "detail": "Login Successfully",
                    "content": {"application/json": {}}
                },
                401: {
                    "detail": "Invalid credentials"
                }
})
async def login(req: LoginReq, db: Session = Depends(get_db)):
    """
    Send email and password to login and retrieve token
    """
    return repository.login(req, db)
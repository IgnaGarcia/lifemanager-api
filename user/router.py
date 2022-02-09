from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from user.model import User, UserBase, UserUpdateReq
from database.db import get_db
from user import repository
from auth.token import current_user, current_admin

users = APIRouter()        


@users.get('/', summary="Retrieve all Users",
           status_code=200, response_model=List[UserBase],
           responses={
               200: {
                   "detail": "Successful Response",
                   "content": {"application/json": {}}
               }
})
async def list_users(db: Session = Depends(get_db), admin= Depends(current_admin)):
    """
    Fetch all user from DB and return.
    """
    return repository.list(db)


@users.get('/{id}', summary="Find User by User UUID",
           status_code=200, response_model=UserBase,
           responses={
               200: {
                   "detail": "Successful Response",
                   "content": {"application/json": {}}
               }
})
async def get_user_by_id(id: str, db: Session = Depends(get_db)):
    """
    Fetch user of this UUID and return. 
    If not exists throw 404 error.

    - **user_id**: id of user to find
    """
    return repository.find(id, db)


@users.post('/', summary="Create new User",
            status_code=201, response_model=UserBase,
            responses={
                201: {
                    "detail": "Created Successfully",
                    "content": {"application/json": {}}
                }
})
async def create_user(user: User, db: Session = Depends(get_db)):
    """
    Create an user with passed data, create his UUID and save to DB.

    - **name**: each user must have a name
    - **email**: unique, used to login
    - **password**: secret, used to login
    - **age**: age of the user
    - **role**: [admin, user]
    """
    return repository.create(user, db)


@users.put('/{id}', summary="Change values of User by UUID",
           status_code=200,
           responses={
               200: { "detail": "Successful Response" }
})
async def update_user(user_updt: UserUpdateReq, id: str, db: Session = Depends(get_db), current_user= Depends(current_user)):
    """
    Fetch user of this UUID, change his values and save to DB, the user updated are returned. 
    If not exists throw 404 error.

    - **user_id**: id of user to find it

    - **name**: each user must have a name
    - **age**: age of the user
    - **role**: [admin, user]
    """
    return repository.update(user_updt, id, db, current_user)


@users.delete('/{id}', summary="Delete User by UUID",
              status_code=200,
              responses={
                  200: { "detail": "Successful Response" }
})
async def delete_user(id: str, db: Session = Depends(get_db), admin= Depends(current_admin)):
    """
    Delete user of this UUID from DB, the user deleted are returned. 
    If not exists throw 404 error.

    - **user_id**: id of user to delete
    """
    return repository.delete(id, db)
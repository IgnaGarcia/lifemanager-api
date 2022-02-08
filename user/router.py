from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import uuid4
from sqlalchemy.orm import Session

from user.model import User, UserUpdateReq, Role
from database.schemas import Users
from database.db import SessionLocal, engine


users = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
responses = {
    403: {"detail": "Not enough privileges"},
    404: {"detail": "Item not found"},
    500: {"detail": "Internal Server Error"}
}


@users.get('/api/users', tags=["Users"],
           status_code=200,
           response_model=List[User],
           summary="Retrieve all Users",
           responses={
               **responses,
               200: {
                   "detail": "Successful Response",
                   "content": {"application/json": {}}
               }
}
)
async def list_users(db: Session = Depends(get_db)):
    """
    Fetch all user from DB and return.
    """
    return db.query(Users).all()


@users.get('/api/users/{user_id}', tags=["Users"],
           status_code=200,
           response_model=User,
           summary="Find User by User UUID",
           responses={
               **responses,
               200: {
                   "detail": "Successful Response",
                   "content": {"application/json": {}}
               }
})
async def get_user_by_id(user_id: str, db: Session = Depends(get_db)):
    """
    Fetch user of this UUID and return. 
    If not exists throw 404 error.

    - **user_id**: id of user to find
    """
    user = db.query(Users).filter(Users.uuid == user_id).first()
    if not user:
        raise HTTPException(status_code= 404, detail= f'User {user_id} not found')
    return user


@users.post('/api/users', tags=["Users"],
            status_code=201,
            response_model=User,
            summary="Create new User",
            responses={
                **responses,
                201: {
                    "detail": "Created Successfully",
                    "content": {"application/json": {}}
                }
})
async def create_user(user: User, db: Session = Depends(get_db)):
    """
    Create an user with passed data, create his UUID and save to DB.

    - **name**: each user must have a name
    - **age**: age of the user
    - **role**: [admin, user]
    """
    user.uuid = str(uuid4())
    new_user = Users(uuid= user.uuid, name= user.name, age= user.age, role= user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@users.put('/api/users/{user_id}', tags=["Users"],
           status_code=200,
           response_model=User,
           summary="Change values of User by UUID",
           responses={
               **responses,
               200: {
                   "detail": "Successful Response",
                   "content": {"application/json": {}}
               }
})
async def update_user(user_updt: UserUpdateReq, user_id: str, db: Session = Depends(get_db)):
    """
    Fetch user of this UUID, change his values and save to DB, the user updated are returned. 
    If not exists throw 404 error.

    - **user_id**: id of user to find it

    - **name**: each user must have a name
    - **age**: age of the user
    - **role**: [admin, user]
    """
    user = db.query(Users).filter(Users.uuid == user_id)
    if not user.first():
        raise HTTPException(status_code= 404, detail= f'User {user_id} not found')
    
    query = {}
    if user_updt.name is not None:
        query['name'] = user_updt.name
    if user_updt.age is not None:
        query['age'] = user_updt.age
    if user_updt.role is not None:
        query['role'] = user_updt.role
        
    user.update(query)
    db.commit()
    return user


@users.delete('/api/users/{user_id}', tags=["Users"],
              status_code=200,
              response_model=User,
              summary="Delete User by UUID",
              responses={
                  **responses,
                  200: {
                      "detail": "Successful Response",
                      "content": {"application/json": {}}
                    }
})
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    """
    Delete user of this UUID from DB, the user deleted are returned. 
    If not exists throw 404 error.

    - **user_id**: id of user to delete
    """
    user = db.query(Users).filter(Users.uuid == user_id)
    if not user: 
        raise HTTPException(status_code= 404, detail= f'User {user_id} not found')
    user.delete(synchronize_session=False)        
    db.commit()
    return user
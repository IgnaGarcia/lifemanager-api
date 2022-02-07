from fastapi import APIRouter
from typing import List
from user.model import User, UserUpdateReq, Role
import user.controller as controller

users = APIRouter()

responses = {
    403: {"description": "Not enough privileges"},
    404: {"description": "Item not found"},
    500: {"description": "Internal Server Error"}
}


@users.get('/api/users', tags=["Users"],
           status_code=200,
           response_model=List[User],
           summary="Retrieve all Users",
           responses={
               **responses,
               200: {
                   "description": "Successful Response",
                   "content": {"application/json": {}}
               }
}
)
async def list_users():
    """
    Fetch all user from DB and return.
    """
    return controller.find_all()


@users.get('/api/users/{user_id}', tags=["Users"],
           status_code=200,
           response_model=User,
           summary="Find User by User UUID",
           responses={
               **responses,
               200: {
                   "description": "Successful Response",
                   "content": {"application/json": {}}
               }
})
async def get_user_by_id(user_id: str):
    """
    Fetch user of this UUID and return. 
    If not exists throw 404 error.

    - **user_id**: id of user to find
    """
    return controller.find(user_id)


@users.post('/api/users', tags=["Users"],
            status_code=201,
            response_model=User,
            summary="Create new User",
            responses={
                **responses,
                201: {
                    "description": "Created Successfully",
                    "content": {"application/json": {}}
                }
})
async def create_user(user: User):
    """
    Create an user with passed data, create his UUID and save to DB.

    - **name**: each user must have a name
    - **age**: age of the user
    - **role**: [admin, user]
    """
    return controller.create(user)


@users.put('/api/users/{user_id}', tags=["Users"],
           status_code=201,
           response_model=User,
           summary="Change values of User by UUID",
           responses={
               **responses,
               200: {
                   "description": "Successful Response",
                   "content": {"application/json": {}}
               }
})
async def update_user(user_updated: UserUpdateReq, user_id: str):
    """
    Fetch user of this UUID, change his values and save to DB, the user updated are returned. 
    If not exists throw 404 error.

    - **user_id**: id of user to find it

    - **name**: each user must have a name
    - **age**: age of the user
    - **role**: [admin, user]
    """
    return controller.put(user_updated, user_id)


@users.delete('/api/users/{user_id}', tags=["Users"],
              status_code=201,
              response_model=User,
              summary="Delete User by UUID",
              responses={
                  **responses,
                  200: {
                      "description": "Successful Response",
                      "content": {"application/json": {}}
                    }
})
async def delete_user(user_id: str):
    """
    Delete user of this UUID from DB, the user deleted are returned. 
    If not exists throw 404 error.

    - **user_id**: id of user to delete
    """
    return controller.delete(user_id)
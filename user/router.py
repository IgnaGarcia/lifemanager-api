from fastapi import APIRouter, HTTPException
from typing import List
from user.model import User, UserUpdateReq, Role
from user.mock import users as usersDB
from uuid import uuid4

users = APIRouter()


@users.get('/api/users', tags = ["Users"], 
           status_code = 200, 
           response_model = List[User], 
           summary = "Retrieve all Users")
async def list_users():
    """
    Retrieve all users
    """

    return usersDB


@users.get('/api/users/{user_id}', tags = ["Users"], 
           status_code = 200, 
           response_model = User, 
           summary = "Find User by User UUID")
async def get_user_by_id(user_id: str):
    """
    Find an user with passed ID:

    - **user_id**: id of user to find
    """

    for user in usersDB:
        if user['uuid'] == user_id:
            return user
    raise HTTPException(status_code = 404, detail = f"User({user_id}) Not Found")


@users.post('/api/users', tags = ["Users"], 
            status_code = 201, 
            response_model = User, 
            summary = "Create new User")
async def create_user(user: User):
    """
    Create an user with passed data:

    - **name**: each user must have a name
    - **age**: age of the user
    - **role**: [admin, user]
    """

    user.uuid = str(uuid4())
    usersDB.append(user.dict())
    
    return user


@users.put('/api/users/{user_id}', tags = ["Users"], 
           status_code = 201, 
           response_model = User, 
           summary = "Change values of User by UUID")
async def update_user(user_updated: UserUpdateReq, user_id: str):
    """
    Find user of UUID, and update with passed values:

    - **user_id**: id of user to find it

    - **name**: each user must have a name
    - **age**: age of the user
    - **role**: [admin, user]
    """

    for user in usersDB:
        if user['uuid'] == user_id:
            if user_updated.name is not None:
                user["name"] = user_updated.name
            if user_updated.age is not None:
                user["age"] = user_updated.age
            if user_updated.role is not None:
                user["role"] = user_updated.role
                
            return user
    raise HTTPException(status_code = 404, detail = f"User({user_id}) Not Found")


@users.delete('/api/users/{user_id}', tags = ["Users"], 
              status_code = 201, 
              response_model = User, 
              summary = "Delete User by UUID")
async def delete_user(user_id: str):
    """
    Delete an user with passed ID:

    - **user_id**: id of user to delete
    """

    for idx, user in enumerate(usersDB):
        if user['uuid'] == user_id:
            
            return usersDB.pop(idx)
    raise HTTPException(status_code = 404, detail = f"User({user_id}) Not Found")

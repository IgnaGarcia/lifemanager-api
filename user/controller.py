from fastapi.responses import JSONResponse
from uuid import uuid4
from user.mock import users
from user.model import User, UserUpdateReq, Role


def find_all():
    return users


def find(id: str):
    for user in users:
        if user['uuid'] == id:
            return user
    return JSONResponse(status_code=404,
                       content={
                           "message": f"User({id}) Not Found"
                       })
    
    
def create(user: User):
    user.uuid = str(uuid4())
    users.append(user.dict())
    return user


def put(user_updt: UserUpdateReq, id: str):
    for user in users:
        if user['uuid'] == id:
            if user_updt.name is not None:
                user["name"] = user_updt.name
            if user_updt.age is not None:
                user["age"] = user_updt.age
            if user_updt.role is not None:
                user["role"] = user_updt.role

            return user
    return JSONResponse(status_code=404, content={
                       "message": f"User({id}) Not Found"})
    

def delete(id: str):
    for idx, user in enumerate(users):
        if user['uuid'] == id:

            return users.pop(idx)
    return JSONResponse(status_code=404, content={
                       "message": f"User({id}) Not Found"})
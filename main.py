from fastapi import FastAPI
from uuid import uuid4
from models import User, UserUpdateReq, Role
from mock import users

tags_metadata = [
    {
        "name": "user",
        "description": "Operations with users."
    }
]

app = FastAPI(
    title = "First API",
    description = "Firt API with FastAPI.",
    contact = {
        "name": "Igna Garcia",
        "url": "https://ignagarcia.vercel.app/",
        "email": "gnachoxp@gmail.com"
    },
    openapi_tags = tags_metadata,
    redoc_url=None
)


@app.get('/')
async def root():
    return {
        "api": "/api", 
        "docs": "/docs"
    }

@app.get('/api/user', tags=["user"])
async def list_users():
    return {
        "message": "succes", 
        "user": users
    }
    
@app.get('/api/user/{user_id}', tags=["user"])
async def get_user_by_id(user_id: str, summary="Find User by User UUID"):
    for user in users:
        if user['id'] == user_id:
            return user
    raise HTTPException(status_code=404, detail=f"User({user_id}) Not Found")

@app.post('/api/user', tags=["user"])
async def create_user(user: User):
    user.uuid = str(uuid4())
    users.append(user.dict())
    return {
        "message": "succes", 
        "user": users
    }
    
@app.put('/api/user/{user_id}', tags=["user"], response_model=User, summary="Change values of User")
async def update_user(user_updated: UserUpdateReq, user_id: str):
    """
    Update an user with passed values:

    - **name**: each user must have a name
    - **age**: age of the user
    - **role**: [admin, user]
    """
    for user in users:
        if user['id'] == user_id:
            if user_updated.name is not None:
                user["name"] = user_updated.name
            if user_updated.age is not None:
                user["age"] = user_updated.age
            if user_updated.role is not None:
                user["role"] = user_updated.role
            return user
    raise HTTPException(status_code=404, detail=f"User({user_id}) Not Found")
    
@app.delete('/api/user/{user_id}', tags=["user"], response_model=User)
async def delete_user(user_id: str):
    for idx,user in enumerate(users):
        if user['id'] == user_id:
            return {
                "message": "succes", 
                "user": users.pop(idx)
            }
    raise HTTPException(status_code=404, detail=f"User({user_id}) Not Found")
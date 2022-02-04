from fastapi import FastAPI
from uuid import uuid4
from models import User
from mock import users

app = FastAPI()
base = "/api"

@app.get('/api/user')
def getUsers():
    return {
        "message": "succes", 
        "user": users
    }
    
@app.get('/api/user/{user_id}')
def getUserById(user_id: str):
    for user in users:
        if user['id'] == user_id:
            return {
                "message": "succes", 
                "user": user
            }
    raise HTTPException(status_code=404, detail=f"User({user_id}) Not Found")

@app.post('/api/user')
def createUser(user: User):
    user.uuid = str(uuid4())
    users.append(user.dict())
    return {
        "message": "succes", 
        "user": users
    }
    
@app.put('/api/user/{user_id}')
def updateUser(user_updated: User, user_id: str):
    for user in users:
        if user['id'] == user_id:
            user["name"] = user_updated.name
            user["age"] = user_updated.age
            return {
                "message": "succes", 
                "user": user
            }
    raise HTTPException(status_code=404, detail=f"User({user_id}) Not Found")
    
@app.delete('/api/user/{user_id}')
def deleteUser(user_id: str):
    for idx,user in enumerate(users):
        if user['id'] == user_id:
            return {
                "message": "succes", 
                "user": users.pop(idx)
            }
    raise HTTPException(status_code=404, detail=f"User({user_id}) Not Found")
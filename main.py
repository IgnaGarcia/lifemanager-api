from fastapi import FastAPI
from user.router import users
from database.db import engine
from database import schemas

schemas.Base.metadata.create_all(bind= engine)
        
tags_metadata = [
    {
        "name": "Users", 
        "description": "Operations with Users."
    }
]
responses = {
    403: {"detail": "Not enough privileges"},
    500: {"detail": "Internal Server Error"}
} 


app = FastAPI(
    title = "First API", 
    description = "Firt API with FastAPI.", 
    contact = {
        "name": "Igna Garcia", 
        "url": "https://ignagarcia.vercel.app/", 
        "email": "gnachoxp@gmail.com"
    }, 
    openapi_tags = tags_metadata, 
    redoc_url = None
)
  
   
app.include_router(users, 
    prefix= '/users', 
    tags= ["Users"], 
    responses = {
        **responses,
        404: {"detail": "User not found"}
    })
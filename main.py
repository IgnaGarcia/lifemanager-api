from fastapi import FastAPI
from user.router import users

tags_metadata = [
    {
        "name": "Base", 
        "description": "Base Operations of API."
    },
    {
        "name": "Users", 
        "description": "Operations with Users."
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
    redoc_url = None
)


@app.get('/', tags = ["Base"])
async def root():
    return {
        "api": "/api", 
        "docs": "/docs"
    }
    
app.include_router(users)
from pydantic import BaseModel

class User(BaseModel):
    uuid: str 
    name: str
    age: int
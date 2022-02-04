from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    uuid: Optional[str]
    name: str
    age: int
from sqlalchemy import Column, Integer, String
from database.db import Base
from user.model import Role

class Users(Base):
    __tablename__ = "users"
    
    uuid = Column(String(255), primary_key=True)
    email = Column(String(255), unique=True)
    name = Column(String(124))
    password = Column(String(255))
    age = Column(Integer)
    role = Column(String(10), default= Role.USER)
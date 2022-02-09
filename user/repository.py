from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from database.schemas import Users
from user.model import User, UserUpdateReq, Role
from util.hash import Hash


def list(db: Session):
    return db.query(Users).all()


def create(user: User, db: Session):
    new_user = Users(uuid= str(uuid4()), 
                     email= user.email,
                     password= Hash.hash(user.password), 
                     name= user.name, 
                     age= user.age, 
                     role= user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def find(id: str, db: Session):
    user = db.query(Users).filter(Users.uuid == id).first()
    if not user:
        raise HTTPException(status_code= 404, detail= f'User {id} not found')
    return user


def update(user_updt: UserUpdateReq, id: str, db: Session, current_user):
    if current_user.uuid != id and current_user.role != Role.ADMIN:
        raise HTTPException(status_code= 403,detail= "Not enough privileges")
        
    user = db.query(Users).filter(Users.uuid == id)
    if not user.first():
        raise HTTPException(status_code= 404, detail= f'User {id} not found')
    
    query = {}
    if user_updt.name is not None:
        query['name'] = user_updt.name
    if user_updt.password is not None:
        query['password'] = Hash.hash(user_updt.password)
    if user_updt.age is not None:
        query['age'] = user_updt.age
    if user_updt.role is not None:
        query['role'] = user_updt.role
        
    user.update(query)
    db.commit()
    return user
    return ""


def delete(id: str, db: Session):
    user = db.query(Users).filter(Users.uuid == id)
    if not user.first(): 
        raise HTTPException(status_code= 404, detail= f'User {id} not found')
    user.delete(synchronize_session=False)        
    db.commit()
    return "ok"

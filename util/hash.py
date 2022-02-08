from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')

class Hash():
    
    def hash(password: str):
        return pwd_cxt.hash(password)
    
    def verify(password: str, hashed: str):
        return pwd_cxt.verify(password, hashed)
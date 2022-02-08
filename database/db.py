from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def engine(host, port, db):
    user = 'root'
    psw = 'admin'
    return create_engine(f'mysql+pymysql://{user}:{psw}@{host}:{port}/{db}')

engine = engine('localhost', 3306, 'life_manager_dev')

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
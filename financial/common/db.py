import os 

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from main import settings


'''
    Database connection utility via sqlalchemy
'''

SQLALCHEMY_DATABASE_URL = settings.DB_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
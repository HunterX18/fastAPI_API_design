from typing import Annotated
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from fastapi import Depends
from app.config import settings


db_name = settings.database_name 
db_user = settings.database_username 
db_password = settings.database_password
db_host = settings.database_hostname

engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
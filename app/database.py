from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

URL = os.getenv("SQLALCHEMY_DATABASE_URL")
if URL is None:
    raise ValueError("No SQLALCHEMY_DATABASE_URL found in environment variables")

engine = create_engine(URL)
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
import sys
from typing import List
from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

from . import models
from .database import engine
from .routers import post, user, auth
########################################################################################
models.Base.metadata.create_all(bind = engine)
app = FastAPI()

try: 
    load_dotenv()
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"), 
        cursor_factory=RealDictCursor
    )

    cursor = conn.cursor()
    print("Connected to the database")
except Exception as error:
    print("Connecting to the database failed: ", error)
    sys.exit(1)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
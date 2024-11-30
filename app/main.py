import time
from typing import List
from fastapi import FastAPI, HTTPException, status, Response, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session
########################################################################################
load_dotenv()

models.Base.metadata.create_all(bind = engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"), 
            cursor_factory=RealDictCursor
        )

        cursor = conn.cursor()
        print("Connected to the database")
        break
    except Exception as error:
        print("Connecting to the database failed: ", error)
        print("Retrying in 5 seconds")
        time.sleep(5)


#################### Create ####################
# Create a new post
@app.post("/posts", status_code = status.HTTP_201_CREATED, response_model = schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#################### Read ####################
# Retrive all posts
@app.get("/posts", response_model = List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

# Retrive a post from an id
@app.get("/posts/{id}", response_model = schemas.PostResponse)
def get_post_by_id(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id), ))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} cannot be found.")
    return post

#################### Update ####################
@app.put("/posts/{id}", response_model = schemas.PostResponse)
def update_post_by_id(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == id)

    if updated_post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} cannot be found.")
    
    updated_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return updated_post.first()

#################### Delete ####################
# Delete a post from an id
@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post_by_id(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id), ))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} cannot be found.")
    
    deleted_post.delete(synchronize_session = False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)
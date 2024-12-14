from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix = "/posts",
    tags = ["Posts"]
)

#################### Create ####################
# Create a new post
@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    new_post.owner_id = current_user.id
    db.add(new_post)
    db.commit()  
    db.refresh(new_post)
    return new_post

#################### Read ####################
# Retrive all posts
@router.get("/", response_model = List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

# Retrive all posts from the current user
@router.get("/current_user", response_model = List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return posts

# Retrive a post from an id
@router.get("/{id}", response_model = schemas.PostResponse)
def get_post_by_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id), ))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} cannot be found.")
    return post

# Retrive a post from an id from the current user
@router.get("/current_user/{id}", response_model = schemas.PostResponse)
def get_post_by_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id), ))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} cannot be found.")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "You are not authorized to perform this action.")
    return post

#################### Update ####################
@router.put("/{id}", response_model = schemas.PostResponse)
def update_post_by_id(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    updated_post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = updated_post_query.first()


    if updated_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} cannot be found.")

    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "You are not authorized to perform this action.")
    
    updated_post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return updated_post

#################### Delete ####################
# Delete a post from an id
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post_by_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id), ))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = deleted_post_query.first()

    if deleted_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} cannot be found.")

    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "You are not authorized to perform this action.")
    
    deleted_post_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)
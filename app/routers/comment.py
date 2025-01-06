from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def comment(
    comment: schemas.CommentBase,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    if not (db.query(models.Post).filter(models.Post.id == comment.post_id).first()):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {comment.post_id} not found.",
        )

    new_comment = models.Comment(**comment.dict(), user_id=current_user.id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return {"message": new_comment}


# Get all comments of a post
@router.get("/{id}", response_model=List[schemas.CommentResponse])
def get_comments(
    id: int,
    db: Session = Depends(get_db),
):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    comments = db.query(models.Comment).filter(models.Comment.post_id == id).all()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found.",
        )
    elif not comments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No comments found for post with id: {id}.",
        )
    return comments


# Get comment by id
@router.get("/comment_id/{id}", response_model=schemas.CommentResponse)
def get_comment(
    id: int,
    db: Session = Depends(get_db),
):
    comment = db.query(models.Comment).filter(models.Comment.id == id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with id: {id} not found.",
        )
    return comment


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    comment = db.query(models.Comment).filter(models.Comment.id == id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with id: {id} not found.",
        )
    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action.",
        )
    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted successfully."}


@router.put("/{id}", response_model=schemas.CommentResponse)
def update_comment(
    id: int,
    comment: schemas.CommentBase,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    updated_comment_query = db.query(models.Comment).filter(models.Comment.id == id)
    updated_comment = updated_comment_query.first()

    if updated_comment == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with id: {id} cannot be found.",
        )

    if updated_comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action.",
        )

    updated_comment_query.update(comment.dict(), synchronize_session=False)
    db.commit()
    return updated_comment

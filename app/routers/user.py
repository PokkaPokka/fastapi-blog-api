from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import re

from .. import models, schemas, utils
from ..database import get_db


router = APIRouter(prefix="/users", tags=["Users"])


#################### Create ####################
@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # validate the password
    if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number",
        )
    else:
        # hash the password
        user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())
    if db.query(models.User).filter(models.User.email == new_user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email: {new_user.email} already exists.",
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


#################### Read ####################
@router.get("/{id}", response_model=schemas.UserResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id: {id} cannot be found.",
        )
    return user


#################### Update ####################
@router.put("/{id}", response_model=schemas.UserResponse)
def update_user(id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user_db = user_query.first()
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id: {id} cannot be found.",
        )

    user_query.update(user.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return user_db

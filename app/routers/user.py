from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db


router = APIRouter(prefix="/users", tags=["Users"])


#################### Create ####################
@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the password
    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())
    if db.query(models.User).filter(models.User.email == new_user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"user with email: {new_user.email} already exists.",
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

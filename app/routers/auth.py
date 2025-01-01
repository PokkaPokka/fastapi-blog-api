from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, utils, schemas, oauth2

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    if user_credentials.username is None or user_credentials.username == "":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Please input your email.",
        )
    elif user_credentials.password is None or user_credentials.password == "":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Please input your password.",
        )

    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )

    if not user or not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with the email or password does not exist.",
        )

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}

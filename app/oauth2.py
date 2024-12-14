from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
import os
from . import schemas, database, models
from sqlalchemy.orm import Session

load_dotenv()
# SECRET_KEY
SECRET_KEY = os.getenv("OAUTH_SECRET_KEY")
# algorithm
ALGORITHM = "HS256"
# expiration time
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credientials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms =[ALGORITHM])
        user_id: str = payload.get("user_id")

        if user_id is None:
            raise credientials_exception
        
        token_data = schemas.TokenData(id = str(user_id))
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise credientials_exception

    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, 
                                          detail = "Could not validate credentials", headers = {"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
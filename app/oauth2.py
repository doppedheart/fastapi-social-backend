from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas,models
from .database import SessionLocal, get_db
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
load_dotenv()
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return token

def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,ALGORITHM)
        id:str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=str(id))
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token:str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token, credentials_exception)
    return token

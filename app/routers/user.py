from fastapi import FastAPI, HTTPException,Response,Depends,APIRouter
from typing import List
from .. import models, schemas,utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Users"]
)


@router.post("/users",status_code=201,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db:Session = Depends(get_db)):
    
    #hash the password 
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    get_user= db.query(models.User).filter(models.User.email == user.email).first()
    if get_user:
        raise HTTPException(status_code=400,detail="Email already registered")
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users",response_model=List[schemas.UserOut])
def get_users(db:Session = Depends(get_db)):
    users= db.query(models.User).all()
    return users

@router.get("/users/{id}",response_model=schemas.UserOut)
def get_single_user(id:int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



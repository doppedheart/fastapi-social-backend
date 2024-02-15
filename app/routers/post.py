from fastapi import FastAPI, HTTPException,Response,Depends,APIRouter
from typing import List
from .. import models, schemas,oauth2
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.Post])
def read_post(db: Session=Depends(get_db)):
    posts= db.query(models.Post).all()
    return posts



@router.get("/sqlalchemy")
def connect_post(db: Session = Depends(get_db)):
    posts= db.query(models.Post).all()
    return {"data": posts}



@router.post("/",status_code=201, response_model=schemas.Post)
def create_post(post:schemas.PostCreate,db : Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.id)
    new_post=models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@router.get("/{id}", response_model=schemas.Post)
def get_single(id:int , db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return  post




@router.delete("/{id}",status_code = 204)
def delete_post(id:int , db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=404, detail="Post not found")
    print(post.owner_id,current_user.id)
    if post.owner_id != int(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=204)




@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int , updated_post:schemas.PostBase, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=404, detail="Post not found")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()


#,get_current_user: int = Depends(oauth2.get_current_user)
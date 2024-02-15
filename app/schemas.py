from pydantic import BaseModel,EmailStr
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase):
    pass

class Post(BaseModel):
    title: str
    content: str
    published: bool
    
    class Config:
        from_attributes = True
        

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
class UserOut(BaseModel):
    id:int
    email: EmailStr
    class Config:
        from_attributes = True
        
class UserLogin(UserCreate):
    pass

class Token(BaseModel):
    access_token:str
    token_type:str
    
    
class TokenData(BaseModel):
    id:Optional[str]= None
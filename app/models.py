from .database import Base
from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
from sqlalchemy import func
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Post(Base):
    __tablename__ = "posts"
    
    id= Column(Integer, primary_key=True, index=True)
    title= Column(String, nullable=False)
    content= Column(String, nullable=False)
    published= Column(Boolean,default=True)
    owner_id =Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    
class User(Base):
    __tablename__ ="users"
    id = Column(Integer,primary_key=True,index=True)
    email =Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)

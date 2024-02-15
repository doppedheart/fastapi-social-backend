from typing import Union, Optional,List
from fastapi import FastAPI, HTTPException,Response,Depends,APIRouter
from fastapi.params import Body
from psycopg2.extras import RealDictCursor
import psycopg2
import time
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from .routers import post,user,auth
from . import models, schemas,utils
from .database import engine,SessionLocal,get_db

models.Base.metadata.create_all(bind=engine)
load_dotenv()
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

# while True:
#     try:
#         conn = psycopg2.connect(
#             dbname="postgres",
#             user="postgres",
#             password="password",
#             host="db",
#             port="5432",
#             cursor_factory=RealDictCursor
#         )
#         cursor = conn.cursor()
#         print("connected")
#     except Exception as error:
#         print("connecting to database failed")
#         print("error:",error)
#         time.sleep(2)

# @app.get("/posts")
# def get_posts():
#     cursor.execute("""SELECT * FROM posts""")
#     posts= cursor.fetchall()
#     return {"data": posts}


# @app.get("/posts/{id}")
# def get_post(id: int):
#     cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id)))
#     post= cursor.fetchone()
#     if not post:
#         raise HTTPException(status_code=404, detail="Post not found")
#     return {"data": post}

# @app.post("/post")
# def create_post(new_post:Post):
#     cursor.execute("""INSERT INTO posts(title,content,published) values(%s,%s,%s) RETURNING *""",(new_post.title,new_post.content,new_post.published))
#     post = cursor.fetchone()
#     conn.commit()
#     return {"data": post}

# @app.delete("/post/{id}")
# def delete_post(id: int):
#     cursor.execute("""DELETE FROM posts WHERE id = %s""",(str(id)))
#     post = cursor.fetchone()
#     conn.commit()
#     return {"success": "Post deleted successfully",
#             "data":post}

# @app.put("/post/{id}")
# def update_post(id: int, post:Post):
#     cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id)))
#     post = cursor.fetchone()
#     conn.commit()
#     return {"data": post}
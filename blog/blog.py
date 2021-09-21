# import need packages
from fastapi import APIRouter,Depends,HTTPException,status
from schemas import schemas
from models import models
from blog import blogcrud
from userapp import user,crud
from config import database
from jose import JWTError, jwt
# from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List,Optional


router=APIRouter( tags=['Blogs']) # instance of APIRouter
get_db=database.get_db # instance of dependency
get_current_user=user.get_current_user # instance current user

# path for get current user blog, get_current_user dependency needs to have a connection to the database
@router.get("/api/mytodos", response_model=List[schemas.Blog])
def get_own_todos(current_user: models.User = Depends(get_current_user),
             	db: Session = Depends(get_db)):
   """return a list of TODOs owned by current user"""
   todos = blogcrud.get_user_todos(db, current_user.id)
   return todos

# path for get current user one blog, get_current_user dependency needs to have a connection to the database
@router.get("/api/mytodos/{todo_id}", response_model=List[schemas.Blog])
def get_todo_one(todo_id: int,current_user:models.User=Depends(get_current_user),db:Session=Depends(get_db)):
    todo=blogcrud.get_one(db,todo_id)
    return todo

# path for create  current user blog, get_current_user dependency needs to have a connection to the database
@router.post("/api/todos", response_model=schemas.ShowBlog)
def add_a_todo(todo_blog: schemas.Blog,
          	current_user: models.User = Depends(get_current_user),
          	db: Session = Depends(get_db)):

   todo = blogcrud.create_blog(db, current_user, todo_blog)
   return todo

# path for update current user blog, get_current_user dependency needs to have a connection to the database
@router.put("/api/todos/{todo_id}", response_model=schemas.Blog)
def update_a_todo(todo_id: int,todo_blog: schemas.Blog,current_user: models.User = Depends(get_current_user),db: Session = Depends(get_db)):
   
#    todo = blogcrud.get_todo(db, todo_id)
   updated_todo = blogcrud.update_todo(todo_id,db,todo_blog)
   return updated_todo

# path for delete current user blog, get_current_user dependency needs to have a connection to the database
@router.delete("/api/todos/{todo_id}")
def delete_a_meal(todo_id: int,
             	current_user: models.User = Depends(get_current_user),
             	db: Session = Depends(get_db)):
   """delete TODO of given id"""
   blogcrud.delete_todo(db, todo_id)
   return {"detail": "TODO Deleted"}



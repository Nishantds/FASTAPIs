# import need packages 
from schemas import schemas
from models import models
from userapp import crud
from config import database
from sqlalchemy.orm import Session
from fastapi import HTTPException,status,Depends


# function for create blog
def create_blog(db: Session, current_user: models.User, todo_blog: schemas.Blog):
   todo = models.Blog(titel=todo_blog.titel,body=todo_blog.body,catagory=todo_blog.catagory)
   todo.creator = current_user
   db.add(todo)
   db.commit()
   db.refresh(todo)
   return todo

# function gor update blog
def update_todo(id:int,db: Session, todo_blog: schemas.Blog):
    todo=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"blog with {id} not found")
    else:
        db.query(models.Blog).filter(models.Blog.id == id).update(todo_blog.dict())  
#    todo.titel = todo_blog.titel
#    todo.body = todo_blog.body
#    todo.catagory = todo_blog.catagory
    db.commit()
    db.refresh(todo)
    return todo

# function for delete blog
def delete_todo(db: Session, id: int):
   todo = db.query(models.Blog).filter(models.Blog.id == id).first()
   db.delete(todo)
   db.commit()
 
#  function for get all blog
def get_user_todos(db: Session, userid: int):
   return db.query(models.Blog).filter(models.Blog.user_id == userid).all()

# function for get one blog by id 
def get_one(db:Session,id:int):
    return db.query(models.Blog).filter(models.Blog.id==id).all()

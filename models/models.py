# SQLAlchemy uses the term "model" to refer to these classes and instances that interact with the database
# SQLAlchemy class "type", as Integer, String, and Boolean, that defines the type in the database, as an argument

from sqlalchemy import Column,Integer,String,ForeignKey

# import (database.py) from config

from config import database

#  use relationship provided by SQLAlchemy ORM.
# that will contain the values from other tables related to this one.
from sqlalchemy.orm import relationship

Base=database.Base


class User(Base):
    __tablename__='users'  # database table name
    id=Column(Integer,primary_key=True)
    name=Column(String(255))
    email=Column(String(255),unique=True)
    password=Column(String(255))  

    blogs=relationship('Blog',back_populates='creator', cascade="all, delete-orphan") 


class Blog(Base):
    __tablename__='blogs' # database table name
    id=Column(Integer,primary_key=True)
    titel=Column(String(255))
    body=Column(String(255))
    catagory=Column(String(255))
    user_id=Column(Integer,ForeignKey('users.id'))
     
    creator=relationship('User',back_populates='blogs') 

'''
 When accessing the attribute blogs in a user. it will have a list
 of blogs SQLAlchemy models (from the blogs table) that have a foreign key pointing to 
 this record in the users table.

'''
'''
And when accessing the attribute creator in an Blog , it will contain a user SQLAlchemy model from the users table. 
It will use the user_id attribute/column with 
its foreign key to know which record to get from the users table.
'''
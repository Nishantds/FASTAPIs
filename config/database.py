# Make connection our mysql database

# SQLAlchemy, the database toolkit for Python
from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base

# sessionmaker provides an "updateable" interface
from sqlalchemy.orm import sessionmaker 



engine=create_engine("mysql+mysqlconnector://root:1234@localhost:3306/test2")

# To create the SessionLocal class, use the function sessionmaker
sessonLocal=sessionmaker(bind=engine,autocommit=False,autoflush=False)

# we will use the function declarative_base() that returns a class.
# we will inherit from this class to create each of the database models or classes (the ORM models):
Base=declarative_base()

# access token time means use can access with token for 30 min
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Our dependency will create a new SQLAlchemy SessionLocal that will be used in a single request,
#  and then close it once the request is finished
def  get_db():
    db=sessonLocal()
    try:
        yield db
    finally:
        db.close()  
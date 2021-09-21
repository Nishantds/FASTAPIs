# OAuth2PasswordRequestForm, which is a part of FastAPI’s security utilities.
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

# For password hashing, we can use Passlib. Let’s define functions that handle password hashing and checking if a password is correct.
from passlib.context import CryptContext
from typing import List,Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from schemas import schemas
from userapp import user
from models import models
from jose import JWTError, jwt #the application actually secure, using JWT tokens and secure password hashing.
import random
import string

# Create a PassLib "context". This is what will be used to hash and verify passwords.

pwd_cxt=CryptContext(schemes=["bcrypt"],deprecated="auto")

# Create a random secret key that will be used to sign the JWT tokens
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

# Create a variable ALGORITHM with the algorithm used to sign the JWT token and set it to "HS256".
ALGORITHM = "HS256"




# Function for verify password
def verify_password(plain_password, hashed_password):  
    return pwd_cxt.verify(plain_password, hashed_password)

# function for get hash password
def get_password_hash(password):
    return pwd_cxt.hash(password)


def get_user(db, email: str):
    return db.query(models.User).filter(models.User.email==email).first()





# function for authenticate user
def authenticate_user(fake_db, email: str, password: str):
    user = get_user(fake_db, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

# function for create access token 
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#  function for create user 
def create_user(db:Session,user:schemas.UserCreate):
    db_user=models.User(name=user.name,email=user.email,password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user    








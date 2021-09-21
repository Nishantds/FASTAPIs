from fastapi import APIRouter,Depends,HTTPException,status
from schemas import schemas
from models import models
from config import database
from userapp import crud
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random
import string

router=APIRouter(tags=['User'])
get_db=database.get_db




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

'''
our path operation functions (request handlers) would then depend on get_current_user.
 The get_current_user dependency needs to have a connection to the database and to hook into the FastAPI’s OAuth2PasswordBearer
  logic to obtain a token
  '''
async def get_current_user(db:Session=Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, crud.SECRET_KEY, algorithms=[crud.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = crud.get_user(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


 
# we will define a Login endpoint and implement the OAuth2 password flow. This endpoint will receive an email and password.
#  We will check the credentials against the database, and on success.

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException( 
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=database.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# path use for get and read current user 
@router.get("/users/me/")
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

# path use for create user dependency needs to have a connection to the database 
@router.post("/users/me/", response_model=schemas.User)
async def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    return crud.create_user(db=db,user=user)


from fastapi import FastAPI ## fastapi is a python class that provides all functionality for your api;
# import need packages
from schemas import schemas
from models import models
from blog import blog
from userapp import user
from config import database
from sqlalchemy.orm import Session

from logging import *

# from .routers import blog,user,authentication
engine=database.engine

app=FastAPI()  #instance of fastapi class 

 # we  add  each APIRouter to the main FastAPI
models.Base.metadata.create_all(engine)

app.include_router(user.router)
app.include_router(blog.router)


# A littel logging module 
@app.on_event("startup")
async def startup_event():
    logger = getLogger("uvicorn.access")
    handler = StreamHandler()
    LOG_FORMAT=handler.setFormatter(Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    basicConfig(filename='logfile.log',level=INFO,filemode='w',format=LOG_FORMAT)
    logger.addHandler(handler)





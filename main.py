from fastapi import FastAPI, Request,Depends## fastapi is a python class that provides all functionality for your api;
# import need packages
from schemas import schemas
from models import models
from blog import blog
from userapp import user
from config import database
from sqlalchemy.orm import Session
from logging.config import dictConfig,fileConfig
from logging import *
from fastapi.logger import logger as fastapi_logger
from logging.handlers import RotatingFileHandler
import uvicorn
from uicheckapp.services import EchoService
import random
import string 
import time



engine=database.engine
models.Base.metadata.create_all(engine)
logger = getLogger(__name__)
 #instance of fastapi class
app=FastAPI()
# we  add  each APIRouter to the main FastAPI
app.include_router(user.router)
app.include_router(blog.router)



fileConfig('my_log.conf', disable_existing_loggers=False)

 

@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")
    
    return response

@app.get("/")
async def root():
    logger.info("logging from the root logger")
    EchoService.echo("hi",'hello')
    return {"status": "alive"}





    
    
    





# create pydantic model
#  Pydantic also uses the term "model" to refer to something different,
#  the data validation, conversion, and documentation classes and instances
# Pydantic models (schemas) that will be used when reading data, when returning it from the API.

from typing import List,Optional

# BaseModel , pydantic provides a dataclass decorator which creates (almost) vanilla python dataclasses with input data parsing and validation.
from pydantic import BaseModel


class BlogBase(BaseModel):
    titel:str
    body:str
    catagory:str
    
    


class Blog(BlogBase):
    class Config():
        orm_mode=True

# Pydantic's orm_mode will tell the Pydantic model to read the data even
#  if it is not a dict, but an ORM model (or any other arbitrary object with attributes)


class User(BaseModel):
    name:str
    email:str
    password:str
    class Config():
        orm_mode=True

class ShowUser(BaseModel):
    name:str
    email:str 
    blogs:List[Blog]=[]
    class Config():
        orm_mode=True  

class ShowBlog(BaseModel):
    # titel:str
    # body:str
    # catagory:str
    creator:ShowUser

    class Config():
        orm_mode=True               


class Token(BaseModel):
    access_token:str
    token_type:str


class TokenData(BaseModel):
    email:Optional[str]=None


class UseInDB(User):
    hashed_password:str

class UserCreate(User):
    password:str    
from datetime import datetime
import uuid
from pydantic import BaseModel,Field


class UserCreateModel (BaseModel):
    username :str = Field(max_length=8)
    email :str = Field(max_length=40)
    password :str = Field(min_length=6)
class User(BaseModel):
    uid:uuid.UUID 
    username:str
    firstName:str
    lastName:str
    email:str
    password_hash: str  = Field(exclude=True)
    is_verified: bool 
    created_at: datetime  
    updated_at: datetime 
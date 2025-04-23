from datetime import datetime
import sqlalchemy.dialects.postgresql as pg
import uuid
from sqlmodel import Column, Field, SQLModel



class User (SQLModel, table = true):
    __tablename__ = "users"

    uid:uuid.UUID
    username:str
    firstName:str
    lastName:str
    email:str
    is_verified: bool  = Field(default=False)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):
        return f' < USER ${self.username} > '
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg
import uuid
from sqlmodel import Column, Field, SQLModel



class User (SQLModel, table = True):
    __tablename__ = "users"


    uid:uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    username:str
    firstName:str
    lastName:str
    email:str
    password_hash: str  = Field(exclude=False)
    role:str = Field(sa_column=Column( pg.VARCHAR,nullable=False, server_default="user"   ))
    is_verified: bool  = Field(default=False)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):
        return f' < USER ${self.username} > '
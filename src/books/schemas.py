import uuid
from pydantic import BaseModel
from datetime import date, datetime
class Book(BaseModel):
    id: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime

class  BookCreateModel (BaseModel):
    
    title:str
    author:str 
    publisher:str
    published_date: date
    page_count:int
    language:str

class BookUpdateModel(BaseModel):
    title:str
    author:str
    publisher:str
    page_count:int
    language:str


# "id": 1,
# "title": "Think Python",
# "author": "Allen B. Downey",
# "publisher": "O'Reilly Media",
# "published_date": "2021-01-01",
# "page_count": 1234,
# "language": "English",
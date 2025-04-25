from typing import List
from fastapi import Depends, FastAPI, Query,HTTPException

from src.books.book_data import books
from src.books.schemas import Book
from src.books.schemas import  BookCreateModel, BookUpdateModel
from fastapi import APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

from src.books.service import BookService
from src.db.main import get_session
from src.auth.dependencies import AccessTokenBearer

book_router = APIRouter()
books_service = BookService()
auth_bearer_token = AccessTokenBearer()


@book_router.get("/", response_model=List[Book])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    user_details = Depends(auth_bearer_token)
    
):
    print(">>>>>>")
    print(user_details)
    books = await books_service.get_all(session)
    print(books)
    return books




@book_router.get('/{book_id}',response_model=Book)
async def read_book(book_id: str,session:AsyncSession = Depends(get_session)):
    book = await books_service.get_book(book_id,session)
    if book:
        return book
    else:
        raise HTTPException(status_code=404, detail="Book not found")
    

@book_router.post("/", status_code=201)
async def create_book(book: BookCreateModel, session: AsyncSession = Depends(get_session)):

    new_book = await books_service.create_book(book, session)
  
    return new_book


@book_router.patch('/{book_id}') 
async def update_book(book_id: str, update_data: BookUpdateModel,session:AsyncSession = Depends(get_session)):
    book = await books_service.update_book(book_id,update_data,session)
    if book:
        return book
    else:
        raise HTTPException(status_code=404, detail="Book not found")



@book_router.delete('/{book_id}',status_code=204)
async def delete_book(book_id: str,session:AsyncSession = Depends(get_session)):
    book = await books_service.delete_book(book_id,session)
    
    if book:
        return book 
    else:

        raise HTTPException(status_code=404, detail="Book not found")


from sqlalchemy.ext.asyncio.session import AsyncSession
from src.books.schemas import  BookCreateModel,BookUpdateModel
from src.db.models import Book

from sqlmodel import select,desc

class BookService :

    
    
    async def get_all(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.execute(statement)
        return result.scalars().all()  # Returns ORM objects

        
        
    async def get_book(self,id:str,session:AsyncSession):

        statement = select(Book).where(Book.id == id )
        result  = await session.execute(statement=statement)
        book =  result.scalars().first()
        return book if book is not None else None

        
        
    async def create_book(self,book_data: BookCreateModel ,session:AsyncSession):

        book_data_dict = book_data.model_dump()
        print("\n ... ")
        print("\n ...  DUMP BOOK -->>> ",book_data_dict)
        print("\n ... ")
        newBook = Book(**book_data_dict)
        session.add(newBook)
        await session.commit()
        return newBook
        pass

    
    
    async def update_book(self,id:str,booke_upd: BookUpdateModel,session:AsyncSession):
        book_to_update = self.get_book(id)
        if book_to_update is not None:
        
            book_data_dict = booke_upd.model_dump()

            for k,v in book_data_dict.items():
                    setattr(book_to_update,k,v)
                    
            await session.commit()
            return book_to_update
        else:
            return None

    
    
    async def delete_book(self,id:str,session:AsyncSession):
        book_to_deleet = await self.get_book(id,session)
        if book_to_deleet is not None:
        
            
            await session.delete(book_to_deleet)
            await session.commit()
            print("SUCCESSS")
            print("SUCCESSS")
            print("SUCCESSS")
            print("SUCCESSS")
            print("SUCCESSS")
            return {"msg":"SUCCESS"}
        else:
            return None


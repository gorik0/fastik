
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.auth.models import User



class UserService :
    async def get_user_by_email(self, email:str, session:AsyncSession) :
        statement = select(User).where(User.email == email)
        result = await  session.execute(statement)
        resp =  result.scalars().first() 
        return resp
    async def user_exists(self, email:str, session:AsyncSession)-> bool :
        user = self.get_user_by_email(email,session)
        return user is not None


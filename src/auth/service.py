
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.auth.models import User
from src.auth.schemas import UserCreateModel
from .utils import generate_hash


class UserService :
    async def get_user_by_email(self, email:str, session:AsyncSession) :
        statement = select(User).where(User.email == email)
        result = await  session.execute(statement)
        resp =  result.scalars().first() 
        return resp
    async def user_exists(self, email:str, session:AsyncSession)-> bool :
        user = await self.get_user_by_email(email,session)

        return True if  user is not None else False
    async def create_user(self, user_create:UserCreateModel, session:AsyncSession)-> bool :
      user_data = user_create.model_dump()
      new_user = User(
          **user_data
      )
      new_user.password_hash = generate_hash(user_data['password'])
      new_user.firstName = "a"
      new_user.lastName = "a"
      new_user.is_verified = True
      new_user.lastName = "a"
      session.add(new_user)
      await session.commit()
      return new_user
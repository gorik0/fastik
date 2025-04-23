from fastapi import APIRouter,Depends,status


from src.auth.schemas import User, UserCreateModel

from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.service import UserService
from src.db.main import get_session
from fastapi.exceptions import  HTTPException

auth_router = APIRouter()


auth_service = UserService()

@auth_router.post('/signup',response_model=User,status_code=status.HTTP_201_CREATED)
async def create_user(user_data :UserCreateModel,session:AsyncSession = Depends(get_session)):

    email = user_data.email
    user_exist  =await auth_service.user_exists(email,session)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=". .. . USER already exist!! .. . . ."
        )
    else:
        new_user = await auth_service.create_user(user_data,session)
        return new_user
from datetime import timedelta
from fastapi import APIRouter,Depends,status


from src.auth.schemas import User, UserCreateModel, UserLoginModel

from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.service import UserService
from src.db.main import get_session
from fastapi.exceptions import  HTTPException

from src.auth.utils import create_token, verify_pass

from fastapi.responses import JSONResponse
auth_router = APIRouter()

REFRESH_EXPIRY_D =2

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
@auth_router.post('/login')
async def create_user(login_data  :UserLoginModel,session:AsyncSession = Depends(get_session)):
    
    user  =await auth_service.get_user_by_email(login_data.email,session)
    if user:
       pass_hash  = verify_pass(login_data.password, user.password_hash)
       if pass_hash:
        
        access_token = create_token(
           user_data={
              'email':user.email,
              'uid':str(user.uid),
           },

        )
        refresh_token = create_token(
           user_data={
              'email':user.email,
              'uid':str(user.uid),
           },
           refresh= True,
           expiry=timedelta(days=REFRESH_EXPIRY_D)

        ) 
        return JSONResponse(
           content={
              "message":"Succe login",
              "access ":access_token,
              "refresh_token ":refresh_token,
              "user_data ":{
                 "email":user.email,
                 "uid":str(user.uid),
              },
           }
        )
       else:
          raise HTTPException(
             detail="invalid pass!!! .. . ..",
             status_code=status.HTTP_403_FORBIDDEN
          )

    else:
        raise HTTPException(
           detail="no user with such an email",
           status_code=status.HTTP_404_NOT_FOUND
        )


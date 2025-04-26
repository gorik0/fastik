import datetime
from datetime import timedelta
from fastapi import APIRouter,Depends,status


from src.auth.dependencies import AccessTokenBearer, RefreshTokenBearer, get_user
from src.auth.schemas import User, UserCreateModel, UserLoginModel

from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.service import UserService
from src.db.main import get_session
from fastapi.exceptions import  HTTPException

from src.auth.utils import create_token, verify_pass

from fastapi.responses import JSONResponse

from src.db.redis import add_jti_to_blocklist
auth_router = APIRouter()



access_bearer_token = AccessTokenBearer()
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



refresh_bearer_token = RefreshTokenBearer()

@auth_router.get("/refresh")
async def refresh(
    token_details:dict  = Depends(refresh_bearer_token)
    
):
   exp = token_details['expire']
   if not exp:
      raise HTTPException(
            detail=" No expire found!!!! ... >>>",
            status_code=status.HTTP_403_FORBIDDEN
         )
   if datetime.datetime.fromtimestamp(int(exp))> datetime.datetime.now():
      new_token = create_token(user_data=token_details['user'])

      await add_jti_to_blocklist(token_details['jti'])

      return JSONResponse(
         content={
            "access_token":new_token
         }
      )
   raise HTTPException(
      detail="Wrong or expired refresh token!!!! ... >>>",
       status_code=status.HTTP_403_FORBIDDEN
   )

@auth_router.get("/logout")
async def logout(
    token_details:dict  = Depends(access_bearer_token)
    
):
   await add_jti_to_blocklist(token_details['jti'])
   return JSONResponse(
      content={
         "message ":"SUCC logout .. "

      },status_code=status.HTTP_200_OK
   )
@auth_router.get("/me")
async def logout(
    user:dict  = Depends(get_user)
):
   if user :
      return user
   else:
      raise HTTPException(
          detail="NO USER WAS FOUND ",
          status_code=status.HTTP_404_NOT_FOUND

      )
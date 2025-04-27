import datetime
from datetime import timedelta
from fastapi import APIRouter,Depends,status


from src import mail
from src.auth.dependencies import AccessTokenBearer, RefreshTokenBearer, RoleChecker, get_user
from src.auth.schemas import PasswordReqModel, PasswordResetConfirmModel, User, UserCreateModel, UserLoginModel

from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.service import UserService
from src.config import Config
from src.db.main import get_session
from fastapi.exceptions import  HTTPException

from src.auth.utils import create_token, create_url_safe_token, decode_url_safe_token, generate_hash, verify_pass

from fastapi.responses import JSONResponse

from src.db.redis import add_jti_to_blocklist
from src.mail import create_message
auth_router = APIRouter()



access_bearer_token = AccessTokenBearer()
REFRESH_EXPIRY_D =2

auth_service = UserService()
role_checker  =Depends(RoleChecker(['user']))

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
              'role':user.role
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
@auth_router.get("/me", dependencies=[role_checker])
async def logout(
    user:dict  = Depends(get_user),
    
):
   if user :
      return user
   else:
      raise HTTPException(
          detail="NO USER WAS FOUND ",
          status_code=status.HTTP_404_NOT_FOUND

      )
   


   # RESET PASSSWORFD!!!!
@auth_router.post("/reset")
async def reset_passw(
    email_to_reset_for: PasswordReqModel,
):
   email= email_to_reset_for.email
   token = create_url_safe_token(data={"email": email})
   link = f'http://{Config.DOMAIN}/api/v1/auth/reset_confirm/{token}'
   html_mess = f"""
Please verify by clicking this link ::: {link}
"""
   msg = create_message(recipients=[email],body=html_mess,subject="RESET PASS")
   await mail.mail.send_message(message=msg)
   return {
      "mesg":"|ok|"
   }


async def reset_account_password(
    token: str,
    passwords: PasswordResetConfirmModel,
    session: AsyncSession = Depends(get_session),
):
    new_password = passwords.password
    confirm_password = passwords.repeat_passw

    if new_password != confirm_password:
        raise HTTPException(
            detail="Passwords do not match", status_code=status.HTTP_400_BAD_REQUEST
        )

    token_data = decode_url_safe_token(token)

    user_email = token_data.get("email")

    if user_email:
        user = await auth_service.get_user_by_email(user_email, session)

        if not user:
            raise HTTPException(detail="NO suer was found ", status_code=status.HTTP_404_NOT_FOUND)

        passwd_hash = generate_hash(new_password)
        await auth_service.update_user(user, {"password_hash": passwd_hash}, session)

        return JSONResponse(
            content={"message": "Password reset Successfully"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "Error occured during password reset."},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
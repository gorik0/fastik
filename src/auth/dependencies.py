from fastapi import Request
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi import HTTPException
from src.auth.utils import decode_token
from fastapi import status
class TokenBearer (HTTPBearer):
    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)
    

    async def __call__(self, request:Request)-> HTTPAuthorizationCredentials|None:
        creds = await super().__call__(request)


        token = creds.credentials

        token_data = decode_token(token=token)

        if token_data is None:
             
            raise HTTPException(
                                status_code=status.HTTP_403_FORBIDDEN,
                                detail="NO data for this token !! >> "
                            )
        self.verify_token_data (token_data)
            
    
        return token_data
    
    def verify_token_data(token_data):
          raise NotImplementedError("NOT implemeent verufy token!!!!")
    

class AccessTokenBearer(TokenBearer):

    def verify_token_data(self,token_data):
          if token_data and  token_data['refresh']:
                raise HTTPException(
                     status_code=status.HTTP_403_FORBIDDEN,
                     detail="Please provide aces token !! >> "
                )
        
class RefreshTokenBearer(TokenBearer):
     def verify_token_data(self,token_data):
          if token_data and not  token_data['refresh']:
                raise HTTPException(
                     status_code=status.HTTP_403_FORBIDDEN,
                     detail="Please provide refresh token !! >> "
                )
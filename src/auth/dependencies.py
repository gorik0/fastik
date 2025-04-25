from fastapi import Request
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi import HTTPException
from src.auth.utils import decode_token
from fastapi import status
class AccessTokenBearer (HTTPBearer):
    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)
    

    async def __call__(self, request:Request)-> HTTPAuthorizationCredentials|None:
        creds = await super().__call__(request)


        token = creds.credentials

        token_data = decode_token(token=token)


        if not self.token_valid:
                raise HTTPException(
                     status_code=status.HTTP_403_FORBIDDEN,
                     detail="Token is invalid!! >> "
                )
        if token_data is None:
              raise HTTPException(
                     status_code=status.HTTP_403_FORBIDDEN,
                     detail="No token data !! >> "
                )
        if token_data['refresh']:
                raise HTTPException(
                     status_code=status.HTTP_403_FORBIDDEN,
                     detail="Please provide aces token !! >> "
                )
        
        return token_data
    def token_valid (self,token:str)->bool:
          token_data = decode_token(token=token)
          return True if token_data is not None else False
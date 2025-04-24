from datetime import timedelta
import logging
import uuid
import jwt
from passlib.context import CryptContext
from src.config import Settings
pass_context = CryptContext(
    schemes=['bcrypt']
)

def generate_hash(password:str)->str:
    hash = pass_context.hash(password)
    return hash

def verify_pass(passw:str, hash:str )-> bool:
    return pass_context.verify(passw,hash)

ACCESS_TOKEN_EXPIRY_SECONDS = 3600
def create_token (user_data : dict , expiry : timedelta, refresh:bool = False):
    payload = {}
    payload['user'] = user_data
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh
    payload['expire'] = expiry if expiry is not None else timedelta(seconds= ACCESS_TOKEN_EXPIRY_SECONDS)
    

    token = jwt.encode(payload=payload,key=Settings.JWT_SECRET,algorithm=Settings.JWT_ALGORITHM)
    return token


def decode_token (token:str)->dict:
    try:

        token_data = jwt.decode(jwt=token,key=Settings.JWT_SECRET,algorithms=Settings.JWT_ALGORITHM)
        return token_data 


    except jwt.PyJWTError as e :
        logging.exception(e )
        return  None

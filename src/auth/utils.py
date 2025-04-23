from passlib.context import CryptContext
pass_context = CryptContext(
    schemes=['bcrypt']
)

def generate_hash(password:str)->str:
    hash = pass_context.hash(password)
    return hash

def verify_pass(passw:str, hash:str )-> bool:
    return pass_context.verify(passw,hash)
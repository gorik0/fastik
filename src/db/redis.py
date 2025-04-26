from src.config import Config
import aioredis

token_blocklist = aioredis.StrictRedis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0
)

JTI_EXPIRY=3600

async def add_jti_to_blocklist (jti):
    await token_blocklist.set(name=jti, value="",ex=JTI_EXPIRY)



async def token_in_blocklist (jti_toget)->bool:
    jti = await token_blocklist.get(name=jti_toget)
    print(" . .. . . .")
    print(" . .. . . .")
    print(" . .. . . .")
    print(jti)
    print(" . .. . . .")
    return jti is not None
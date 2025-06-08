import redis.asyncio as redis
from src.config import Config
JTI_EXPIRY = 3600  # 1 hour

# token_blocklist = redis.Redis(
#     host=Config.REDIS_HOST,
#     port=Config.REDIS_PORT,
#     password=Config.REDIS_PASSWORD,  # Add the password for authentication
#     decode_responses=True,
# )
token_blocklist = redis.from_url(
    Config.REDIS_URL,
    decode_responses=True,
)
# jti means JWT ID
async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(
        name=jti,
        value="",
        ex=JTI_EXPIRY,
        )

async def token_in_blocklist(jti: str) -> bool:
    jti = await token_blocklist.get(jti)
    return jti is not None
    # if jti:
    #     return True
    # else:
    #     return False

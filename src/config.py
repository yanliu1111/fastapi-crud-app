from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import asyncpg
import os
import src.config as Config


load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
    MAIL_USERNAME=Config.MAIL_USERNAME,
    MAIL_PASSWORD=Config.MAIL_PASSWORD,
    MAIL_FROM=Config.MAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER=Config.MAIL_SERVER,
    MAIL_FROM_NAME=Config.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,

settings = Settings()
# test the Neon connection
async def connect_to_neon():
    """Function to test PostgreSQL connection to Neon."""
    try:
        async with asyncpg.create_pool(settings.DATABASE_URL) as pool:
            async with pool.acquire() as conn:
                time = await conn.fetchval('SELECT NOW();')
                version = await conn.fetchval('SELECT version();')
        print('Current time:', time)
        print('PostgreSQL version:', version)
    except Exception as e:
        print("Error connecting to PostgreSQL:", e)

Config = settings
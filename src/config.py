from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import asyncpg
import os

load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    DOMAIN: str
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_nested_delimiter="__"
    )

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
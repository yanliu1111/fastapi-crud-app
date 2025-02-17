from sqlmodel import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine
from src.config import Config

# Remove sslmode from DATABASE_URL
database_url = Config.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://").split("?")[0]

# Create an asynchronous engine using the PostgreSQL URL from the config
engine = create_async_engine(
    url=database_url,
    echo=True
)

async def init_db():
    async with engine.begin() as conn:
        statement = text("SELECT 'Hello, World!';")
        result = await conn.execute(statement)
        print(result.all())
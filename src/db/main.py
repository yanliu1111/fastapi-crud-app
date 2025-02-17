from sqlmodel import create_engine, text, SQLModel, Field, Column
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import sessionmaker
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
        # statement = text("SELECT 'Hello, World!';")
        # result = await conn.execute(statement)
        # print(result.all())
        from src.books.models import Book
        await conn.run_sync(SQLModel.metadata.create_all)

# if you want to set service.py as an dependency injection, you can do session: AsyncSession = Depends(get_session)
async def get_session() -> AsyncSession:
    Session = sessionmaker(
        bind= async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with Session() as session:
        yield session
# what __init__.py does is to make the code in the src folder a package

from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db

@asynccontextmanager
async def life_span(app: FastAPI):
    print (f"Starting the app...")
    await init_db()
    yield
    print (f"App hasbeen stopped")

version = "v1"
app = FastAPI(
    title="Bookly",
    description="A REST API for books review web service",
    version=version,
    lifespan=life_span
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"]) #prefix is optional

# what __init__.py does is to make the code in the src folder a package

from fastapi import FastAPI, Depends, status
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.auth.routers import auth_router
from src.reviews.routes import review_router
from src.tags.routes import tags_router
from .error import register_all_errors

@asynccontextmanager
async def life_span(app: FastAPI):
    print (f"Starting the app...")
    from src.db.main import Book
    await init_db()
    yield
    print (f"App hasbeen stopped")

version = "v1"
app = FastAPI(
    title="Bookly",
    description="A REST API for books review web service",
    version=version,
    # lifespan=life_span # lifespan is a context manager that runs when the app starts and stops
)

register_all_errors(app)  # Register all custom error handlers

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"]) #prefix is optional
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"]) 
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["reviews"])
app.include_router(tags_router, prefix=f"/api/{version}/tags", tags=["tags"])

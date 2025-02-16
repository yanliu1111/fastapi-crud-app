# what __init__.py does is to make the code in the src folder a package

from fastapi import FastAPI
from src.books.routes import book_router
version = "v1"
app = FastAPI(
    title="Bookly",
    description="A REST API for books review web service",
    version=version,
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"]) #prefix is optional

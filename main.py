from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException

from typing import List

app = FastAPI()

books = [
  {
    "id": 1,
    "title":"Test Title",
    "author" : "Test Author",
    "publisher": "Test Publications",
    "published_date":"2024-12-10",
    "page_count": 215,
    "language": "en",
  },
  {
    "id": 2,
    "title":"Test Title 2",
    "author" : "Test Author 2",
    "publisher": "Test Publications 2",
    "published_date":"2024-01-10",
    "page_count": 220,
    "language": "cn",
  },
  {
    "id": 3,
    "title":"Test Title 3",
    "author" : "Test Author 3",
    "publisher": "Test Publications 3",
    "published_date":"2024-05-10",
    "page_count": 200,
    "language": "fr",
  }
]




@app.get("/books", response_model=List[Book])
async def get_books():
    return books

@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data:Book)-> dict:
    new_book = book_data.model_dump() #converts the pydantic model to a dictionary
    books.append(new_book)
    return new_book

@app.get("/book/{book_id}")
async def get_book(book_id: int) -> dict:
    for book in books:
        if book["id"] == book_id:
            return book 
    # return {"message": "Book not found"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@app.patch("/book/{book_id}")
async def update_book(book_id: int, book_update_data:BookUpdateModel) -> dict:
    for book in books:
        if book["id"] == book_id:
            book['title'] = book_update_data.title
            book['author'] = book_update_data.author
            book['publisher'] = book_update_data.publisher
            book['page_count'] = book_update_data.page_count
            book['language'] = book_update_data.language
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@app.delete("/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int): # do not return anything, no need -> dict
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
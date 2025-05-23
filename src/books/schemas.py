from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import Optional, List
from src.reviews.schemas import ReviewModel


class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: datetime
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime

    # class Config:
    #     orm_mode = True

class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: datetime
    page_count: int
    language: str

class BookDetailModel(Book):
    reviews: List[ReviewModel]

class BookUpdateModel(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    page_count: Optional[int] = None
    language: Optional[str] = None

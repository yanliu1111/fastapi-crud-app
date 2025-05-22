from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import uuid
from typing import Optional
from src.auth import models


class Book(SQLModel, table=True):
    __tablename__ = "books"
    uid: uuid.UUID = Field(sa_column=Column(
        pg.UUID,
        nullable=False,
        primary_key=True,
        default=uuid.uuid4
    ))
    title: str
    author: str
    publisher: str
    published_date: datetime
    page_count: int
    language: str
    user_uid:Optional [uuid.UUID] = Field(default=None, foreign_key="users.uid")
    created_at: datetime = Field(sa_column = Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column = Column(pg.TIMESTAMP, default=datetime.now))
    user: Optional['models.User'] = Relationship(back_populates="books")
    # __repr__ method to return a string representation of the Book object
    def __repr__(self):
        return f"<Book {self.title}>"
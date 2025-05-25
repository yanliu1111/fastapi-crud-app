from sqlmodel import SQLModel, Field, Column, Relationship
import uuid
from datetime import datetime, date
import sqlalchemy.dialects.postgresql as pg
from typing import List, Optional


class User(SQLModel, table=True):
    __tablename__ = "users"
    uid: uuid.UUID = Field(sa_column=Column(
        pg.UUID,
        nullable=False,
        primary_key=True,
        default=uuid.uuid4
    ))
    username: str
    email: str
    first_name: str
    last_name: str
    role: str = Field(sa_column=Column(pg.VARCHAR(50), nullable=False, server_default="user"))
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    password_hash: str = Field(exclude=True)
    created_at: datetime = Field(sa_column = Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column = Column(pg.TIMESTAMP, default=datetime.now))
    books: List['Book'] = Relationship(back_populates="user", sa_relationship_kwargs={'lazy': 'selectin'})
    reviews: List['Review'] = Relationship(back_populates="user", sa_relationship_kwargs={'lazy': 'selectin'})
    
    def __repr__(self):
        return f"<User {self.username}>"
    
class BookTage(SQLModel, table=True):
    book_id: uuid.UUID = Field(default=None, foreign_key="books.uid", primary_key=True)
    tag_id: uuid.UUID = Field(default=None, foreign_key="tags.uid", primary_key=True)

class Tag (SQLModel, table=True):
    __tablename__ = "tags"
    uid: uuid.UUID = Field(sa_column=Column(
        pg.UUID,
        nullable=False,
        primary_key=True,
        default=uuid.uuid4
    ))
    name: str = Field(sa_column=Column(pg.VARCHAR(50), nullable=False, unique=True))
    created_at: datetime = Field(sa_column = Column(pg.TIMESTAMP, default=datetime.now))
    books: List['Book'] = Relationship(
        back_populates="tags",
        bool_populates="tags",
        sa_relationship_kwargs={'lazy': 'selectin'},
    )
    def __repr__(self) -> str:
        return f"<Tag {self.name}>"

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
    reviews: List['Review'] = Relationship(back_populates="book", sa_relationship_kwargs={'lazy': 'selectin'})
    user: Optional[User] = Relationship(back_populates="books")
    
    def __repr__(self):
        return f"<Book {self.title}>"

class Review(SQLModel, table=True):
    __tablename__ = "reviews"
    uid: uuid.UUID = Field(sa_column=Column(
        pg.UUID,
        nullable=False,
        primary_key=True,
        default=uuid.uuid4
    ))
    rating: int = Field(lt=5)
    review_text: str
    user_uid:Optional [uuid.UUID] = Field(default=None, foreign_key="users.uid")
    book_uid:Optional [uuid.UUID] = Field(default=None, foreign_key="books.uid")
    created_at: datetime = Field(sa_column = Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column = Column(pg.TIMESTAMP, default=datetime.now))
    user: Optional[User] = Relationship(back_populates="reviews")
    book: Optional[Book] = Relationship(back_populates="reviews")
    
    def __repr__(self):
        return f"<Review for book {self.book_uid} by user {self.user_uid}>"
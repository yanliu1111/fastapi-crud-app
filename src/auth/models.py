from sqlmodel import SQLModel, Field, Column, Relationship
import uuid
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg
from typing import List
from src.books import models


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
    books: List['models.Book'] = Relationship(back_populates="user", sa_relationship_kwargs={'lazy': 'selectin'})

    def __repr__(self):
        return f"<User {self.username}>"
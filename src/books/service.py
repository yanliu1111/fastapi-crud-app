from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreateModel, BookUpdateModel
from sqlmodel import select, desc
from .models import Book

class BookService:
  async def get_books(self, session:AsyncSession):
    statement = select(Book).order_by(desc(Book.created_at))
    result = await session.exec(statement)
    return result.all()
  async def get_book(self, book_uid:str, session:AsyncSession):
    statement = select(Book).where(Book.uid == book_uid)
    result = await session.exec(statement)
    book = result.first()
    return book if book is not None else None
  async def create_book(self, book_data:BookCreateModel, session:AsyncSession):
    # create a dictionary of the book data
    book_data_dict = book_data.model_dump()
    # create a new book object from the dictionary
    new_book = Book(**book_data_dict)
    session.add(new_book)
    await session.commit() # commit the transaction
    await session.refresh(new_book)
    return new_book

  async def update_book(self, book_uid:str, update_data:BookUpdateModel, session:AsyncSession):
    book_to_update = await self.get_book(book_uid, session)
    if book_to_update is not None:
      # check if the book exists
      update_data_dict = update_data.model_dump()
      # update the book object with the new data
      for key, value in update_data_dict.items():
        setattr(book_to_update, key, value)
      await session.commit()
      await session.refresh(book_to_update)
      return book_to_update
    return None
  async def delete_book(self, book_uid:str, session:AsyncSession):
    book_to_delete = await self.get_book(book_uid, session)
    if book_to_delete is not None:
      await session.delete(book_to_delete)
      await session.commit()
    else:
      return None
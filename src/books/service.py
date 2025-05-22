from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreateModel, BookUpdateModel
from sqlmodel import select, desc
from .models import Book
from datetime import datetime
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
  
  async def create_book(
        self, book_data: BookCreateModel, 
        user_id: str, session: AsyncSession
    ):
     # create a dictionary of the book data
    book_data_dict = book_data.model_dump()
    # create a new book object from the dictionary
    new_book = Book(**book_data_dict)

    # new_book.published_date = datetime.strptime(
    #             book_data_dict["published_date"], "%Y-%m-%d"
    #         )
    new_book.published_date = book_data_dict["published_date"]
    new_book.user_uid = user_id

    session.add(new_book)
    await session.commit()  # commit the transaction

    return new_book

  async def update_book(self, book_uid: str, update_data: BookUpdateModel, session: AsyncSession):
    book_to_update = await self.get_book(book_uid, session)
    if book_to_update is not None:
        # Check if the book exists
        update_data_dict = update_data.model_dump()

        # Update the book object with the new data
        for key, value in update_data_dict.items():
            setattr(book_to_update, key, value)
        # Explicitly update updated_at
        book_to_update.updated_at = datetime.now()

        await session.commit()
        await session.refresh(book_to_update)

        # DEBUG: Convert the SQLAlchemy model to a dictionary before returning
        return book_to_update
        # if i didnt wrote down the response model = Book in the routes.py PATCH method, i would have to return the dictionary like this:
        # return {
        #     "uid": str(book_to_update.uid),
        #     "title": book_to_update.title,
        #     "author": book_to_update.author,
        #     "publisher": book_to_update.publisher,
        #     "page_count": book_to_update.page_count,
        #     "language": book_to_update.language,
        #     "created_at": book_to_update.created_at,
        #     "updated_at": book_to_update.updated_at
        # }
  
  async def delete_book(self, book_uid: str, session: AsyncSession):
    book_to_delete = await self.get_book(book_uid, session)
    
    if book_to_delete is not None:
        await session.delete(book_to_delete)
        await session.commit()
        return {"message": "Book successfully deleted"}
    else:
        return None
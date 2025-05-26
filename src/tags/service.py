from src.db.models import Tag
from src.books.service import BookService
from src.tags.schemas import TagAddModel, TageCreateModel

from fastapi import status
from fastapi.exceptions import HTTPException

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc

from src.error import BookNotFound, TagNotFound, TagAlreadyExists

book_service = BookService()
server_error = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
from sqlmodel.ext.asyncio.session import AsyncSession

class TagService:
    async def get_tags(self, session: AsyncSession):
        statement = select(Tag).order_by(desc(Tag.created_at))
        result = await session.exec(statement)
        return result.all()
    
    async def add_tags_to_book(self, book_uid: str, tag_data: TagAddModel, session: AsyncSession):
        book = await book_service.get_book_by_uid(book_uid, session)
        if not book:
            raise BookNotFound(book_uid)

        for tag_item in tag_data.tags:
            result = await session.exec(
                select(Tag).where(Tag.name == tag_item.name)
            )
            tag = result.one_or_none()
            if not tag:
                tag = Tag(name=tag_item.name)
            
            book.tags.append(tag)
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book
    
    async def 
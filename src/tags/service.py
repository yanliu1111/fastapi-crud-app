from src.db.models import Tag
from src.books.service import BookService
from src.tags.schemas import TagAddModel, TagCreateModel

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
    
    async def add_tag(self, tag_data: TagCreateModel, session: AsyncSession):
        statement = select(Tag).where(Tag.name == tag_data.name)
        result = await session.exec(statement)
        tag = result.first()
        if tag:
            raise TagAlreadyExists(tag_data.name)
        new_tag = Tag(name=tag_data.name)

        session.add(new_tag)
        await session.commit()
        await session.refresh(new_tag)
        return new_tag
    
    async def get_tag_by_uid(self, tag_uid: str, session: AsyncSession):
        statement = select(Tag).where(Tag.uid == tag_uid)
        result = await session.exec(statement)
        tag = result.first() # different from .one_or_none() to raise an error if not found

    async def update_tag(self, tag_uid, tag_update_data: TagCreateModel, session: AsyncSession):
        tag = await self.get_tag_by_uid(tag_uid, session) # AsyncSession method means it will raise an error if not found
        if not tag:
            raise TagNotFound(tag_uid)
        update_data_dict = tag_update_data.model_dump() # model_dump() converts the Pydantic model to a dictionary
        for key, value in update_data_dict.items():
            setattr(tag, key, value)
            await session.commit()
            await session.refresh(tag)
        return tag
    
    async def delete_tag(self, tag_uid: str, session: AsyncSession):
        tag = await self.get_tag_by_uid(tag_uid, session)
        if not tag:
            raise TagNotFound(tag_uid)
        await session.delete(tag)
        await session.commit()
        return {"message": "Tag deleted successfully"}
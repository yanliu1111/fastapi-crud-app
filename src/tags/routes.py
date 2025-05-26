from fastapi import APIRouter, Depends, status
from .service import TagService
from src.auth.dependencies import RoleChecker
from src.db.main import get_session
from .schemas import TagModel, TagCreateModel, TagAddModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.error import TagNotFound, TagAlreadyExists
from typing import List
from src.books.schemas import Book


tags_router = APIRouter()
tag_service = TagService()
user_role_checker = Depends(RoleChecker(["admin", "user"]))

@tags_router.get(
    "/",
    response_model=list[TagModel],
    status_code=status.HTTP_200_OK,
    dependencies=[user_role_checker],
)
async def get_all_tags(session: AsyncSession = Depends(get_session)):
    """
    Get all tags.
    """
    tags = await tag_service.get_tags(session)
    return tags

@tags_router.post(
    "/",
    response_model=TagModel,
    status_code=status.HTTP_201_CREATED,
    dependencies=[user_role_checker],
)
async def add_tag (tag_data: TagCreateModel, session: AsyncSession = Depends(get_session)) -> TagModel:
    """
    Add a new tag.
    """
    tag_added = await tag_service.add_tag(tag_data=tag_data, session=session)
    return tag_added

@tags_router.post(
    "/book/{book_uid}/tags",
    response_model=Book,
    status_code=status.HTTP_201_CREATED,
    dependencies=[user_role_checker],
)
async def add_tags_to_book(
    book_uid: str,
    tag_data: TagAddModel,
    session: AsyncSession = Depends(get_session),
) -> Book:
    """
    Add tags to a book.
    """
    book_with_tag = await tag_service.add_tags_to_book(book_uid=book_uid, tag_data=tag_data, session=session)
    return book_with_tag

@tags_router.put(
    "/{tag_uid}",
    response_model=TagModel,
    status_code=status.HTTP_200_OK,
    dependencies=[user_role_checker],
) -> TagModel:
async def update_tag(
    tag_uid: str,
    tag_update_data: TagCreateModel,
    session: AsyncSession = Depends(get_session),
) -> TagModel:
    """
    Update a tag.
    """
    tag = await tag_service.get_tag_by_uid(tag_uid, session)
    if not tag:
        raise TagNotFound(tag_uid)
    
    updated_tag = await tag_service.update_tag(tag_uid, tag_update_data, session)
    return updated_tag

@tags_router.delete(
    "/{tag_uid}",
    status_code=status.HTTP_204_NO_CONTENT, #204 means No Content
    dependencies=[user_role_checker],
)
async def delete_tag(
    tag_uid: str,
    session: AsyncSession = Depends(get_session),
)-> None:
    """
    Delete a tag.
    """
    update_tag = await tag_service.delete_tag(tag_uid, session)
    return update_tag

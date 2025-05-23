from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from .schemas import Book, BookUpdateModel, BookCreateModel, BookDetailModel
from src.db.main import get_session
from src.auth.dependencies import AccessTokenBearer, RoleChecker
import time

book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(['admin', 'user']))

@book_router.get("/", response_model=List[Book], dependencies=[role_checker])   
async def get_books(session: AsyncSession = Depends(get_session),
                    token_details: dict = Depends(access_token_bearer),
                    # _:bool = Depends(role_checker):
                    ) -> dict:
    print("token_details", token_details)
    books = await book_service.get_books(session)
    return books

@book_router.get("/user/{user_id}", response_model=List[Book], dependencies=[role_checker])   
async def get_user_books_submission(
    user_id: str,  # Match the path parameter name
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
) -> dict:
    print("token_details", token_details)
    print(f"user_id: {user_id}")
    books = await book_service.get_user_books(user_id, session)  # Use user_id here
    return books

# @book_router.get(
#     "/user/{user_uid}", response_model=List[Book], dependencies=[role_checker]
# )

@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book, dependencies=[role_checker])
async def create_a_book(book_data: BookCreateModel, 
                         user_id: str = Depends(AccessTokenBearer()),
                        session: AsyncSession = Depends(get_session), 
                        token_details: dict = Depends(access_token_bearer)
                        ) -> dict:
    user_id = token_details['user']['user_uid'] # Corrected dictionary access
    new_book = await book_service.create_book(book_data, user_id, session)
    print(f"new_book: {repr(new_book)}")
    time.sleep(1)  # Introduce a short delay to ensure print gets executed
    return new_book


@book_router.get("/{book_uid}", response_model=BookDetailModel, dependencies=[role_checker])
async def get_book(book_uid: str, session: AsyncSession = Depends(get_session), token_details: dict = Depends(access_token_bearer), dependencies=[role_checker]) -> dict:
    book = await book_service.get_book(book_uid, session)
    if book:
        return  book.model_dump()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@book_router.patch("/{book_uid}", response_model=Book, dependencies=[role_checker])
async def update_book(book_uid: str, book_update_data:BookUpdateModel, session: AsyncSession = Depends(get_session),token_details: dict = Depends(access_token_bearer)) -> dict:
    updated_book = await book_service.update_book(book_uid, book_update_data, session)
    if updated_book:
        return updated_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker])
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session),token_details: dict = Depends(access_token_bearer)):
    deleted_book = await book_service.delete_book(book_uid, session)
    if deleted_book:
        return None
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
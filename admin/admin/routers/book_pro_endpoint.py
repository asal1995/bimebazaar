from fastapi import HTTPException, Depends
import httpx

from admin.core.security import get_current_user, User, role_required
from admin.db.enums import Role
from admin.schemas.book_schema import BookCreate
from admin.provider.book_provider import BookProvider
from admin.core.errors import CustomException
from fastapi import APIRouter

route = APIRouter()


# Dependency
def get_book_provider():
    return BookProvider()


@route.post("/books/")
@role_required([Role.admin.value])
async def create_book(
        book: BookCreate,
        provider: BookProvider = Depends(get_book_provider),
        admin: User = Depends(get_current_user)):
    try:
        return await provider.create_book(book)
    except CustomException as e:
        e.http_response()


@route.put("/books/{book_id}/")
@role_required([Role.admin.value])
async def update_book(
        book_id: int, book: BookCreate,
        provider: BookProvider = Depends(get_book_provider),
        admin: User = Depends(get_current_user)
):
    try:
        return await provider.update_book(book, book_id)
    except CustomException as e:
        e.http_response()


@route.delete("/books/{book_id}/")
@role_required([Role.admin.value])
async def delete_book(
        book_id: int,
        provider: BookProvider = Depends(get_book_provider),
        admin: User = Depends(get_current_user)):
    try:
        return await provider.delete_book(book_id)
    except CustomException as e:
        e.http_response()

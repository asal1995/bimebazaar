from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from books.core.errors import CustomException, ok
from books.core.config import Settings, get_settings
from ..core.security import verify_key
from redis.asyncio import Redis
from ..db.database import get_async_db, get_redis
from ..schemas.books_schema import Book, BookCreate
from ..services.books_service import create_book_service, update_book_service, delete_book_service, \
    detail_books_service, list_books_service

route = APIRouter()


@route.post("/", dependencies=[Depends(verify_key)])
async def create_book_endpoint(book: BookCreate, db: AsyncSession = Depends(get_async_db)):
    try:
        new_book = await create_book_service(book=book, db=db)
        return new_book
    except CustomException as e:
        return e.http_response()


@route.put("/{book_id}/", dependencies=[Depends(verify_key)], response_model=Book)
async def update_book_endpoint(book_id: int, book: BookCreate, db: AsyncSession = Depends(get_async_db)):
    try:
        updated_book = await update_book_service(book=book, book_id=book_id, db=db)
        return updated_book
    except CustomException as e:
        return e.http_response()


@route.delete("/{book_id}/", dependencies=[Depends(verify_key)])
async def delete_book_endpoint(book_id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        await delete_book_service(book_id=book_id, db=db)
        return ok()
    except CustomException as e:
        return e.http_response()


@route.get("/detail/{book_id}/")
async def get_detail_book_endpoint(book_id: int,
                                   db: AsyncSession = Depends(get_async_db),
                                   env: Settings = Depends(get_settings)):
    response = await detail_books_service(book_id=book_id, db=db, env=env)
    return response


@route.get("/list/")
async def get_list_book_endpoint(db: AsyncSession = Depends(get_async_db),
                                 env: Settings = Depends(get_settings),
                                 redis: Redis = Depends(get_redis)
                                 ):
    result = await list_books_service(db=db, env=env, redis=redis)
    return result
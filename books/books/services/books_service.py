from books.core.errors import BadRequest, ErrorCode, NotFound
from books.db.crud import create_book, get_book, update_book, delete_book, get_books_list
from books.schemas.books_schema import BookCreate, BookUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from redis.asyncio import Redis
from books.provider.bcr_provider import get_comment_and_rating
from books.core.config import config
from books.core.errors import BadRequest


async def create_book_service(book: BookCreate, db: AsyncSession):
    try:
        return await create_book(db, book)
    except Exception as e:
        logger.error(f"error in create book:{book.title}>>{e}")
        raise BadRequest(ErrorCode.CREATE_BOOK_ERROR)


async def update_book_service(book: BookCreate, book_id: int, db: AsyncSession):
    db_book = await get_book(db=db, book_id=book_id)
    if not db_book:
        raise NotFound(ErrorCode.BOOK_NOT_FOUND)
    try:
        await update_book(db=db, db_book=db_book, book=book)
        return db_book

    except Exception as e:
        logger.error(f"error in update book:{book.title}>>{e}")
        raise BadRequest(ErrorCode.UPDATE_BOOK_ERROR)


async def delete_book_service(book_id: int, db: AsyncSession):
    try:
        book = await get_book(db=db, book_id=book_id)
        if book:
            await delete_book(db=db, db_book=book)
            return
        raise NotFound(ErrorCode.BOOK_NOT_FOUND)
    except Exception as e:
        logger.error(f"error in delete book:{book_id}>>{e}")
        raise BadRequest(ErrorCode.DELETE_BOOK_ERROR)


async def list_books_service(db: AsyncSession, redis: Redis, env: config):
    books = await get_books_list(db=db)
    books_with_bookmarks = []
    for book in books:
        detail = f"{env.detail_url.strip('/')}/{book.id}/"
        bookmark_count = await redis.get(f"book:{book.id}:bookmarks") or 0
        books_with_bookmarks.append({
            "id": book.id,
            "title": book.title,
            "bookmark_count": int(bookmark_count),
            "book_detail": detail
        })
    return books_with_bookmarks


async def detail_books_service(book_id: int, db: AsyncSession, env: config):
    book = await get_book(db=db, book_id=book_id)
    if not book:
        raise NotFound(ErrorCode.BOOK_NOT_FOUND)
    try:
        cr: dict = await get_comment_and_rating(book_id=book_id, env=env)
        cr['book_description'] = book.description

        return {'detail': cr}
    except Exception as e:
        logger.error(f"error in calling bcr service for detail book:{book_id}>>{e}")
        raise BadRequest(ErrorCode.BCR_PROVIDER_ERROR)

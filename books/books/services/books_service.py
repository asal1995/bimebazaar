from books.core.errors import BadRequest, ErrorCode, NotFound
from books.db.crud import create_book, get_book, update_book, delete_book
from books.schemas.books_schema import BookCreate, BookUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger


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

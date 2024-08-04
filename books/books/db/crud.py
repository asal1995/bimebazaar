from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from books.db.models import Book
from books.schemas.books_schema import BookCreate


async def get_book(db: AsyncSession, book_id: int):
    result = await db.execute(select(Book).filter(Book.id == book_id))
    return result.scalar_one_or_none()


async def create_book(db: AsyncSession, book: BookCreate):
    db_book = Book(**book.dict())
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book


async def update_book(db: AsyncSession, db_book, book: BookCreate):
    for key, value in book.dict().items():
        setattr(db_book, key, value)
    await db.commit()
    await db.refresh(db_book)
    return db_book


async def delete_book(db: AsyncSession, db_book: int):
    await db.delete(db_book)
    await db.commit()

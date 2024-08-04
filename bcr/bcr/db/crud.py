from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from bcr.db.models import CommentRating, Bookmark
from bcr.schemas.comment_rate_schema import CommentRateCreate
from bcr.core.errors import CustomException


async def get_comment_rate(db: AsyncSession, user_id: int, book_id: int):
    result = await db.execute(select(CommentRating).filter(
        CommentRating.user_id == user_id, CommentRating.book_id == book_id))  # noqa
    return result.scalar_one_or_none()


async def create_comment_rate(db: AsyncSession, body: dict):
    db_comment = CommentRating(body)
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment


async def update_comment_rate(db: AsyncSession, db_record, body: dict):
    for key, value in body.items():
        setattr(db_record, key, value)
    await db.commit()
    await db.refresh(db_record)
    return db_record


async def get_bookmark(db: AsyncSession, book_id: int, user_id: int):
    result = await db.execute(select(
        Bookmark).filter(Bookmark.book_id == book_id, Bookmark.user_id==user_id))    # noqa
    return result.scalars().first()


async def create_bookmark(db: AsyncSession, bookmark: dict):
    db_bookmark = Bookmark(**bookmark)
    db.add(db_bookmark)
    await db.commit()
    await db.refresh(db_bookmark)
    return db_bookmark


async def delete_bookmark(db: AsyncSession, db_bookmark: int):
    await db.delete(db_bookmark)
    await db.commit()

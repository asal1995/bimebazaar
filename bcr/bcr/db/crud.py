from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, case, Integer

from bcr.db.enums import RatingEnum
from bcr.db.models import CommentRating, Bookmark
from bcr.schemas.comment_rate_schema import CommentRateCreate
from bcr.core.errors import CustomException



async def get_comment_rate(db: AsyncSession, user_id: int, book_id: int):
    result = await db.execute(select(CommentRating).filter(
        CommentRating.user_id == user_id, CommentRating.book_id == book_id))  # noqa
    return result.scalar_one_or_none()


async def create_comment_rate(db: AsyncSession, body: dict):
    db_comment = CommentRating(**body)
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
        Bookmark).filter(Bookmark.book_id == book_id, Bookmark.user_id == user_id))  # noqa
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


# async def get_comment_count(db: AsyncSession, book_id: int):
#     comments = await db.execute(
#         select(func.count(CommentRating.id)).filter(
#             CommentRating.book_id == book_id,  # noqa
#             CommentRating.comment.isnot(None)
#         )
#     )
#     comments_count = comments.scalar()
#     return comments_count


async def get_comment_rate_count(db: AsyncSession, book_id: int):
    result = await db.execute(
        select(
            func.count(CommentRating.rating).label("ratings_count"),
            func.avg(
                case(
                     (CommentRating.rating == RatingEnum.ONE, 1),
                            (CommentRating.rating == RatingEnum.TWO, 2),
                            (CommentRating.rating == RatingEnum.THREE, 3),
                            (CommentRating.rating == RatingEnum.FOUR, 4),
                            (CommentRating.rating == RatingEnum.FIVE, 5),
                )
            ).label("average_rating"),
            func.count(CommentRating.id).label("comment_count"),

        ).filter(
            CommentRating.book_id == book_id,
            CommentRating.rating.isnot(None)
        )
    )
    result = result.one()
    res = dict(ratings_count=result.ratings_count,
               average_rating=result.average_rating,
               comments_count=result.comment_count)
    return res


# async def get_count_rate(db: AsyncSession, user_id: int, book_id: int):
#     ratings_count = await db.execute(
#         select(func.count(CommentRating.id)).filter(
#             CommentRating.book_id == book_id,  # noqa
#             CommentRating.rating.isnot(None)
#         )
#     )
#     ratings_count = ratings_count.scalar()
#     return ratings_count


async def get_ratings_distribution(db: AsyncSession, book_id: int):
    ratings_distributed = await db.execute(
        select(CommentRating.rating, func.count(CommentRating.id)).filter(
            CommentRating.book_id == book_id,
            CommentRating.rating.isnot(None)
        ).group_by(CommentRating.rating)
    )
    ratings_distribution = {rating: count for rating, count in ratings_distributed.all()}
    return ratings_distribution


async def get_user_comment_ratings(db: AsyncSession, book_id: int):
    results = await db.execute(
        select(CommentRating.user_id, CommentRating.comment, CommentRating.rating).filter(
            CommentRating.book_id == book_id,
        ).order_by(CommentRating.user_id)
    )
    return results

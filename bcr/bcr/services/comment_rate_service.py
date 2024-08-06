from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from bcr.core.errors import BadRequest, ErrorCode
from bcr.db.crud import create_comment_rate, get_comment_rate, update_comment_rate, get_bookmark, delete_bookmark, \
    get_comment_rate_count, get_ratings_distribution, get_user_comment_ratings
from bcr.db.models import CommentRating
from bcr.schemas.comment_rate_schema import CommentRateCreate, UserCommentsRatings, BookStats, CommentRatingSchema


async def create_comment_rate_service(db: AsyncSession,
                                      body: CommentRateCreate,
                                      user_id: int,
                                      ):
    bookmark = await get_bookmark(db=db, book_id=body.book_id, user_id=user_id)
    if bookmark:
        await delete_bookmark(db=db, db_bookmark=bookmark)
    try:
        data = body.model_dump()
        data['user_id'] = user_id
        record = await get_comment_rate(db=db, user_id=user_id, book_id=body.book_id)
        if record:
            await update_comment_rate(db=db, db_record=record, body=data)
            return
        await create_comment_rate(db=db, body=data)
        return
    except Exception as e:
        logger.error(f"error in create comment with user: {user_id}")
        raise BadRequest(ErrorCode.CREATE_COMMENT_ERROR)


async def get_book_state_service(db: AsyncSession, book_id: int):
    user_data = {}
    user_comments_ratings = []
    # average and count comment and rating
    comment_rate = await get_comment_rate_count(db=db, book_id=book_id)
    # rated distributed by rate
    rating_distributed = await get_ratings_distribution(db=db, book_id=book_id)
    # rated distributed by user
    user_comment_rate = await get_user_comment_ratings(db=db, book_id=book_id)
    for user_id, comment, rating in user_comment_rate:
        if user_id not in user_data:
            user_data[user_id] = {"comments-rating": []}
        if comment is not None:
            user_data[user_id]["comments-rating"].append(CommentRatingSchema(user_id=user_id, book_id=book_id,
                                                                             rating=rating,  comment=comment))

    for user_id, data in user_data.items():
        user_comments_ratings.append(UserCommentsRatings(
            user_id=user_id,
            comments_rating=data["comments-rating"],
        ))
    return BookStats(
        book_id=book_id,
        comments_count=comment_rate['comments_count'],
        ratings_count=comment_rate['ratings_count'],
        average_rating=comment_rate['average_rating'],
        ratings_distribution=rating_distributed,
        user_comments_ratings=user_comments_ratings
    )

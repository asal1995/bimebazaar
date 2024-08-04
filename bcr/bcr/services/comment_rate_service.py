from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from bcr.core.errors import BadRequest, ErrorCode
from bcr.db.crud import create_comment_rate, get_comment_rate, update_comment_rate, get_bookmark, delete_bookmark
from bcr.schemas.comment_rate_schema import CommentRateCreate


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

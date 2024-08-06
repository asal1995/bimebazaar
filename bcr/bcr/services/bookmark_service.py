
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from bcr.db.crud import create_bookmark, get_comment_rate
from bcr.core.errors import BadRequest, ErrorCode


async def create_bookmark_service(db: AsyncSession, user_id: int, book_id: int):
    rate_or_comment = await get_comment_rate(db=db, user_id=user_id, book_id=book_id)
    if rate_or_comment:
        raise BadRequest(ErrorCode.BOOK_WAS_READ_BEFORE)
    data = dict(user_id=user_id, book_id=book_id)
    try:
        await create_bookmark(db=db, bookmark=data)
        return
    except Exception as e:
        logger.error(f'error in bookmark creation for '
                     f'user_id: {user_id}, book_id: {book_id}: {e}')
        raise BadRequest(ErrorCode.BOOKMARKED_ERROR)

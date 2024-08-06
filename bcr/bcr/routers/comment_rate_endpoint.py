from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from bcr.core.errors import CustomException, ok
from bcr.core.security import get_current_user, verify_key, User
from bcr.db.database import get_async_db
from bcr.schemas.comment_rate_schema import CommentRateCreate, BookStats
from bcr.services.comment_rate_service import create_comment_rate_service, get_book_state_service

route = APIRouter()


@route.post('/react/')
async def create_comment_rate_endpoint(body: CommentRateCreate,
                                       db: AsyncSession = Depends(get_async_db),
                                       user: User = Depends(get_current_user)
                                       ):
    try:
        await create_comment_rate_service(db=db, user_id=user.user_id, body=body)
        return ok()
    except CustomException as e:
        return e.http_response()


@route.get("/stats/{book_id}/", dependencies=[Depends(verify_key)], response_model=BookStats)
async def get_book_stats_endpoint(book_id: int, db: AsyncSession = Depends(get_async_db)):
    return await get_book_state_service(db, book_id)

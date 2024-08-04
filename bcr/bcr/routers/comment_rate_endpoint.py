from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from bcr.core.errors import CustomException, ok
from bcr.core.security import get_current_user
from bcr.db.database import get_async_db
from bcr.schemas.comment_rate_schema import CommentRateCreate
from bcr.services.comment_rate_service import create_comment_rate_service

route = APIRouter()


@route.post('/react/')
async def create_comment_rate_endpoint(body: CommentRateCreate,
                                       db: AsyncSession = Depends(get_async_db),
                                       user_id: int = Depends(get_current_user)
                                       ):
    try:
        await create_comment_rate_service(db=db, user_id=user_id, body=body)
        return ok()
    except CustomException as e:
        return e.http_response()

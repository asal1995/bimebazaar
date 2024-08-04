from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from bcr.core.errors import CustomException, ok
from bcr.core.security import get_current_user
from bcr.db.database import get_async_db
from bcr.services.bookmark_service import create_bookmark_service

route = APIRouter()


@route.post('/bookmark/')
async def create_bookmark(book_id: int, db: AsyncSession = Depends(get_async_db),
                          user_id: int = Depends(get_current_user)):
    try:
        await create_bookmark_service(db=db, user_id=user_id, book_id=book_id)
    except CustomException as e:
        return e.http_response()



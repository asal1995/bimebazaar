from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from users.core.errors import ok
from users.db.database import get_async_db
from users.schemas.user_schema import UserCreateSchema
from users.services.login_service import register_or_login
from users.core.errors import CustomException
from users.core.config import get_settings, config

route = APIRouter()


@route.post("/sign_in/")
async def register_or_login_route(
        user_credentials: UserCreateSchema,
        db: AsyncSession = Depends(get_async_db),
        env: config = Depends(get_settings),):
    try:
        result = await register_or_login(user_data=user_credentials, db=db, env=env)
        return ok(result)
    except CustomException as e:
        return e.http_response()

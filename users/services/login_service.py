from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from users.core import config
from users.core.authentication import create_access_token
from users.schemas.user_schema import UserCreateSchema
from passlib.context import CryptContext

from users.core.errors import BadRequest, ErrorCode, Unauthorized
from users.db.crud import get_user_by_email, create_new_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def register_or_login(user_data: UserCreateSchema, db: AsyncSession, env: config):
    db_user = await get_user_by_email(email=user_data.email, db=db)

    if db_user:
        if pwd_context.verify(user_data.password, db_user.hashed_password):
            if db_user.is_active:
                data = dict(sub=db_user.email, user_id=str(db_user.id), user_type=db_user.type_.name)
                access_token = create_access_token(data=data, env=env)
                return {"access_token": access_token, "token_type": "bearer"}
            else:
                raise BadRequest(ErrorCode.USER_DOSE_NOT_ACTIVE)
        else:
            raise Unauthorized(ErrorCode.INVALID_CREDENTIALS)
    else:
        # Register new user
        hashed_password = pwd_context.hash(user_data.password)
        db_user = await create_new_user(email=user_data.email, password=hashed_password, db=db)
        data = dict(sub=db_user.email, user_id=str(db_user.id), user_type=db_user.type_.name)
        access_token = create_access_token(data=data, env=env)
        return {"access_token": access_token, "token_type": "bearer"}


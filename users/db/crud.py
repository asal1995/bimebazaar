from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from users.db.models import User


async def get_user_by_email(email: str, db: AsyncSession):
    db_user = await db.execute(select(User).filter(User.email == email))
    return db_user.scalars().first()


async def create_new_user(email: str, password: str,  db: AsyncSession):
    new_user = User(email=email, hashed_password=password, is_active=False)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

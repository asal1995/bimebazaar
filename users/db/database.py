from loguru import logger
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from users.core.config import get_settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

settings = get_settings()

async_engine = create_async_engine(settings.async_db_url, echo=True)
AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)
logger.info("Init async Database from address: %s" % async_engine.url.host)

# Base class for declarative models
Base = declarative_base()


def get_async_conn():
    async_engine.connect()
    return async_engine.url.database


async def get_async_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

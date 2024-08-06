from loguru import logger
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from books.core.config import get_settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
import redis.asyncio as redis


async def get_redis() -> redis.Redis:
    redis_client = redis.from_url("redis://localhost:6379", encoding="utf-8", decode_responses=True)
    return redis_client


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


async def get_redis() -> redis.Redis:
    red_cli = await redis.from_url(url=settings.redis_url, encoding="utf-8", decode_responses=True)
    return red_cli

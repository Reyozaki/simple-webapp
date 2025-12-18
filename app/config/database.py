from sqlalchemy.ext.asyncio import create_async_engine

from app.config.settings import settings

ASYNC_DB_URL = settings.async_db_url

async_engine = create_async_engine(
    ASYNC_DB_URL,
    pool_size=20,
    max_overflow=5,
    echo=False,
)

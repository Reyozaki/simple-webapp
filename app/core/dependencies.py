from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import async_engine


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session."""
    async with AsyncSession(async_engine) as session:
        yield session


# Asynchronous database session dependency for dependency injection
DBSession = Annotated[AsyncSession, Depends(get_db_session)]


class Pagination:
    """Pagination model for list with 10 rows of data"""

    def __init__(
        self,
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=1, le=100),
    ):
        self.page = page
        self.size = size
        self.offset = (page - 1) * size


def get_pagination(pagination: Pagination = Depends()) -> Pagination:
    """Get pagination object"""
    return pagination

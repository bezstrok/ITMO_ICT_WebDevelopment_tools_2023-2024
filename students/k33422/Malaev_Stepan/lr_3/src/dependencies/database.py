import typing as tp

from sqlalchemy.ext.asyncio.session import AsyncSession

from ..services.database import Database

__all__ = [
    "AsyncSession",
    "get_database_session",
]


async def get_database_session() -> tp.AsyncGenerator[AsyncSession, None]:
    async with Database.session() as session:
        yield session

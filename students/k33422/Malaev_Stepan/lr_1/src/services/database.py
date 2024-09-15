import typing as tp
import functools
from contextlib import asynccontextmanager

import orjson
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)

from .. import config

__all__ = ["Database"]

T = tp.TypeVar("T", bound=tp.Callable[..., tp.Awaitable[tp.Any]])

engine = create_async_engine(
    config.postgres.url,
    echo=False,
    json_serializer=orjson.dumps,
    json_deserializer=orjson.loads,
)
session_maker = async_sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


class Database:
    @classmethod
    @asynccontextmanager
    async def session(cls) -> tp.AsyncGenerator[AsyncSession, None]:
        async with session_maker() as session:
            try:
                yield session
            except SQLAlchemyError:
                await session.rollback()
                raise

    @classmethod
    def with_session(cls, method: T) -> T:
        @functools.wraps(method)
        async def wrapper(*args: tp.Any, session: tp.Optional[AsyncSession] = None, **kwargs: tp.Any) -> tp.Any:
            if session is None:
                async with cls.session() as session:
                    return await method(*args, session=session, **kwargs)
            return await method(*args, session=session, **kwargs)

        return tp.cast(T, wrapper)

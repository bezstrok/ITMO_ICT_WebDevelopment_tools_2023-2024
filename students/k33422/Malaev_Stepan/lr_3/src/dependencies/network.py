import typing as tp

import aiohttp
from aiohttp import ClientSession

__all__ = [
    "ClientSession",
    "get_client_session",
]


async def get_client_session() -> tp.AsyncGenerator[ClientSession, None]:
    async with aiohttp.ClientSession() as session:
        yield session

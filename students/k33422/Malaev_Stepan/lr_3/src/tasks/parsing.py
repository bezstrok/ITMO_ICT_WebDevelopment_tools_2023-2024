import typing as tp
import random
import asyncio

from taskiq import TaskiqDepends
import aiohttp

from .. import models, dependencies, schemas
from ..worker import broker
from ..services.network import get_usernames_from_github
from ..services.authorization import hash_password

__all__ = ["parse_users"]

_default_password = "password"


def _randomize(username: str) -> str:
    return f"{username}_{random.randint(100, 999)}"


@broker.task
async def parse_users(
    pages: int,
    client_session: tp.Annotated[aiohttp.ClientSession, TaskiqDepends(dependencies.get_client_session)],
    database_session: tp.Annotated[dependencies.AsyncSession, TaskiqDepends(dependencies.get_database_session)],
) -> dict[str, tp.Any]:
    tasks = [get_usernames_from_github(page, client_session=client_session) for page in range(pages)]
    list_usernames: list[list[str]] = await asyncio.gather(*tasks)  # noqa
    usernames = [username for usernames in list_usernames for username in usernames]

    await models.User.create_many(
        [dict(username=_randomize(username), hashed_password=hash_password(_default_password)) for username in usernames],
        session=database_session,
    )
    await database_session.commit()

    return schemas.ParseUsersGetDTO(count=len(usernames)).model_dump()

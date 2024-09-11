from .redis import Redis
from .postgres import Postgres
from .api import API

__all__ = [
    "redis",
    "postgres",
    "api",
]

redis = Redis()  # type: ignore
postgres = Postgres()  # type: ignore
api = API()  # type: ignore

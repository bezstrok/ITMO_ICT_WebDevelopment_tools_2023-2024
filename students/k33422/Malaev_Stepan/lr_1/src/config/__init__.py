from .redis import Redis
from .postgres import Postgres
from .api import API
from .authorization import Authorization

__all__ = [
    "redis",
    "postgres",
    "api",
    "authorization",
]

redis = Redis()  # type: ignore
postgres = Postgres()  # type: ignore
api = API()  # type: ignore
authorization = Authorization()  # type: ignore

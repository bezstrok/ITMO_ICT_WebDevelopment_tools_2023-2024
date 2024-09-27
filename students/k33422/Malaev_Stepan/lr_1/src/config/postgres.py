from pydantic import PostgresDsn
from pydantic_settings import SettingsConfigDict

from . import base

__all__ = ["Postgres"]


class Postgres(base.Base):
    host: str
    port: int
    user: str
    password: str
    database: str

    model_config = SettingsConfigDict(env_prefix="pg_")

    @property
    def url(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                path=self.database,
            )
        )

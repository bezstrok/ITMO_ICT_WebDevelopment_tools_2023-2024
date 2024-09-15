from pydantic import RedisDsn
from pydantic_settings import SettingsConfigDict

from . import base

__all__ = ["Redis"]


class Redis(base.Base):
    host: str
    port: int
    password: str

    model_config = SettingsConfigDict(env_prefix="rd_")

    @property
    def url(self) -> str:
        return str(
            RedisDsn.build(
                scheme="redis",
                password=self.password,
                host=self.host,
                port=self.port,
            )
        )

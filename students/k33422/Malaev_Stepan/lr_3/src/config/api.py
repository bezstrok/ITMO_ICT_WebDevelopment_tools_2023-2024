from pydantic import HttpUrl
from pydantic_settings import SettingsConfigDict

from . import base

__all__ = ["API"]


class API(base.Base):
    host: str
    port: int

    model_config = SettingsConfigDict(env_prefix="ap_")

    @property
    def url(self) -> str:
        return str(
            HttpUrl.build(
                scheme="http",
                host=self.host,
                port=self.port,
            )
        )

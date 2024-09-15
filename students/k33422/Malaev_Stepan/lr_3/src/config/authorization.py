import functools

from pydantic_settings import SettingsConfigDict

from . import base

__all__ = ["Authorization"]


class Authorization(base.Base):
    algorithm: str
    access_token_expires_in: int
    refresh_token_expires_in: int
    private_key_path: str
    public_key_path: str

    model_config = SettingsConfigDict(env_prefix="au_")

    @functools.cached_property
    def private_key(self) -> str:
        return self._read_file(self.private_key_path)

    @functools.cached_property
    def public_key(self) -> str:
        return self._read_file(self.public_key_path)

    @staticmethod
    def _read_file(path: str) -> str:
        with open(path, "r") as file:
            return file.read()

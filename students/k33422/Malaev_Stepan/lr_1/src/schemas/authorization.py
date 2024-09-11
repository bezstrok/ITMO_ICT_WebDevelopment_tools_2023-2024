from datetime import datetime

from . import base

__all__ = [
    "Payload",
    "AccessTokenDTO",
    "CredentialsDTO",
]


class Payload(base.Base):
    id: int
    typ: str
    exp: datetime
    iat: datetime


class AccessTokenDTO(base.Base):
    access_token: str


class CredentialsDTO(base.Base):
    username: str
    password: str

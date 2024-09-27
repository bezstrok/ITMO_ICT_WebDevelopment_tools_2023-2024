from datetime import datetime

from . import base

__all__ = [
    "Payload",
    "AccessTokenDTO",
    "CredentialsDTO",
    "ChangePasswordDTO",
]


class Payload(base.Base):
    sub: int
    typ: str
    exp: datetime
    iat: datetime


class AccessTokenDTO(base.Base):
    access_token: str


class CredentialsDTO(base.Base):
    username: str
    password: str


class ChangePasswordDTO(base.Base):
    old_password: str
    new_password: str

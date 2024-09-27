import typing as tp

from pydantic import EmailStr

from . import base

__all__ = [
    "UserGetDTO",
    "UserUpdateDTO",
]


class UserGetDTO(base.Base):
    id: int
    username: str
    email: tp.Optional[str]


class UserUpdateDTO(base.Base):
    email: EmailStr

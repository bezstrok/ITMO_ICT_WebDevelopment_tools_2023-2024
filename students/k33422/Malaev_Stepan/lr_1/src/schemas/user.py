import typing as tp

from . import base

__all__ = ["UserGetDTO"]


class UserGetDTO(base.Base):
    id: int
    username: str
    email: tp.Optional[str]

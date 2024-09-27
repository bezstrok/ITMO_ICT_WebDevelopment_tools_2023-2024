import typing as tp

from . import base

__all__ = [
    "ParseUsersCreateDTO",
    "ParseUsersGetDTO",
    "Task",
]

T = tp.TypeVar("T")


class ParseUsersCreateDTO(base.Base):
    pages: int


class ParseUsersGetDTO(base.Base):
    count: int


class Task(base.Base, tp.Generic[T]):
    id: str
    result: tp.Optional[T]

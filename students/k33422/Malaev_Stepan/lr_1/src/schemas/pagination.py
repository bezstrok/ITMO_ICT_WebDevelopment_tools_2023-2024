import typing as tp

from . import base

__all__ = ["Page"]

T = tp.TypeVar("T")


class Page(base.Base, tp.Generic[T]):
    count: int
    next: int | None
    previous: int | None
    results: list[T]

import typing as tp

from .. import models, schemas


__all__ = ["Paginator"]

_default_page_size = 10
_page_size_attr = "__page_size__"

T = tp.TypeVar("T")


class Paginator:
    @classmethod
    def paginate(cls, model: type[models.Base], results: tp.Sequence[T], page: int) -> schemas.Page[T]:
        count = len(results)
        size = getattr(model, _page_size_attr, _default_page_size)

        return schemas.Page[T](
            count=count,
            next=page + 1 if count >= size else None,
            previous=page - 1 if page > 1 else None,
            results=list(results),
        )

    @classmethod
    def page_to_limit_offset(cls, model: type[models.Base], page: int) -> tuple[int, int]:
        size = getattr(model, _page_size_attr, _default_page_size)

        return size, (page - 1) * size

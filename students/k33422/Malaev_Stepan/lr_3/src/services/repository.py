import typing as tp

from sqlalchemy.orm.attributes import QueryableAttribute
from sqlalchemy.sql.elements import BinaryExpression, UnaryExpression
from sqlalchemy.sql import operators, extract
from sqlalchemy import sql

__all__ = ["Repository"]

T = tp.TypeVar("T")

_operators: dict[str, tp.Callable[[tp.Any, tp.Any], tp.Any]] = {
    "isnull": lambda c, v: (c == None) if v else (c != None),  # noqa
    "exact": operators.eq,
    "ne": operators.ne,  # not equal or is not (for None)
    "gt": operators.gt,  # greater than , >
    "ge": operators.ge,  # greater than or equal, >=
    "lt": operators.lt,  # lower than, <
    "le": operators.le,  # lower than or equal, <=
    "in": operators.in_op,
    "notin": operators.notin_op,
    "between": lambda c, v: c.between(v[0], v[1]),
    "like": operators.like_op,
    "ilike": operators.ilike_op,
    "startswith": operators.startswith_op,
    "istartswith": lambda c, v: c.ilike(v + "%"),
    "endswith": operators.endswith_op,
    "iendswith": lambda c, v: c.ilike("%" + v),
    "contains": lambda c, v: c.ilike("%{v}%".format(v=v)),
    "year": lambda c, v: extract("year", c) == v,
    "year_ne": lambda c, v: extract("year", c) != v,
    "year_gt": lambda c, v: extract("year", c) > v,
    "year_ge": lambda c, v: extract("year", c) >= v,
    "year_lt": lambda c, v: extract("year", c) < v,
    "year_le": lambda c, v: extract("year", c) <= v,
    "month": lambda c, v: extract("month", c) == v,
    "month_ne": lambda c, v: extract("month", c) != v,
    "month_gt": lambda c, v: extract("month", c) > v,
    "month_ge": lambda c, v: extract("month", c) >= v,
    "month_lt": lambda c, v: extract("month", c) < v,
    "month_le": lambda c, v: extract("month", c) <= v,
    "day": lambda c, v: extract("day", c) == v,
    "day_ne": lambda c, v: extract("day", c) != v,
    "day_gt": lambda c, v: extract("day", c) > v,
    "day_ge": lambda c, v: extract("day", c) >= v,
    "day_lt": lambda c, v: extract("day", c) < v,
    "day_le": lambda c, v: extract("day", c) <= v,
}
_operator_splitter = "__"
_operator_default = "exact"
_desc_prefix = "-"


class Repository:
    @classmethod
    def build_django_filters(cls, model: type[T], filters: tp.Mapping[str, tp.Any]) -> list[BinaryExpression[T]]:
        expressions: list[BinaryExpression[T]] = []

        for key, value in filters.items():
            if _operator_splitter in key:
                attr, operator = key.rsplit(_operator_splitter, 1)
                column = getattr(model, attr)
            else:
                column = getattr(model, key)
                operator = _operator_default

            if column is None:
                raise ValueError(f"Column {key} not found in model {model.__name__}")
            if operator not in _operators:
                raise ValueError(f"Operator {operator} not found")

            expressions.append(_operators[operator](column, value))

        return expressions

    @classmethod
    def build_django_orders(cls, model: type[T], orders: tp.Sequence[str]) -> list[UnaryExpression[T]]:
        expressions: list[UnaryExpression[T]] = []

        for attr in orders:
            if attr.startswith(_desc_prefix):
                column = getattr(model, attr[1:])
                fn = sql.desc
            else:
                column = getattr(model, attr)
                fn = sql.asc

            if column is None:
                raise ValueError(f"Column {attr} not found in model {model.__name__}")

            expressions.append(fn(column))

        return expressions

    @classmethod
    def build_fields(cls, model: type[T], fields: tp.Sequence[str]) -> list[QueryableAttribute[T]]:
        expressions: list[QueryableAttribute[T]] = []

        for attr in fields:
            column = getattr(model, attr)
            if column is None:
                raise ValueError(f"Column {attr} not found in model {model.__name__}")

            expressions.append(column)

        return expressions

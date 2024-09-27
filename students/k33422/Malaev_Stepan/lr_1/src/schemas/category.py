import typing as tp

from . import base
from .budget import BudgetGetDTO

__all__ = [
    "CategoryCUDTO",
    "CategoryGetOneDTO",
    "CategoryGetManyDTO",
]


class CategoryCUDTO(base.Base):
    title: str
    parent_id: tp.Optional[int]
    budget_id: tp.Optional[int]


class CategoryGetOneDTO(base.Base):
    id: int
    title: str
    parent: tp.Optional[tp.Self]
    children: list[tp.Self]
    budget: tp.Optional[BudgetGetDTO]


class CategoryGetManyDTO(base.Base):
    id: int
    title: str
    parent_id: tp.Optional[int]
    budget_id: tp.Optional[int]

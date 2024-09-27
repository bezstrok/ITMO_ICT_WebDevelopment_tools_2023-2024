import typing as tp

from sqlalchemy import orm, types

from . import base, mixins

if tp.TYPE_CHECKING:
    from .transaction import Transaction
    from .category import Category
    from .budget import Budget

__all__ = ["User"]


class User(mixins.PrimaryKeyIDMixin, base.Base):
    username: orm.Mapped[str] = orm.mapped_column(types.String(32), unique=True, nullable=False)
    hashed_password: orm.Mapped[str] = orm.mapped_column(types.String(128), nullable=False)
    email: orm.Mapped[str] = orm.mapped_column(types.String(128), nullable=True)

    transactions: orm.Mapped[list["Transaction"]] = orm.relationship(back_populates="user")
    categories: orm.Mapped[list["Category"]] = orm.relationship(back_populates="user")
    budgets: orm.Mapped[list["Budget"]] = orm.relationship(back_populates="user")

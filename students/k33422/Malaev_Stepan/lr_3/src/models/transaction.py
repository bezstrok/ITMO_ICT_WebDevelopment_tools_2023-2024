import typing as tp

from sqlalchemy import orm, types, schema

from . import base, mixins
from .. import enums

if tp.TYPE_CHECKING:
    from .user import User
    from .category import Category

__all__ = ["Transaction"]


class Transaction(mixins.CreatedAtMixin, mixins.PrimaryKeyIDMixin, base.Base):
    user_id: orm.Mapped[int] = orm.mapped_column(schema.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    amount: orm.Mapped[float] = orm.mapped_column(types.Numeric(10, 2), nullable=False)
    transaction_type: orm.Mapped[enums.TransactionType] = orm.mapped_column(types.Enum(enums.TransactionType), nullable=False)

    user: orm.Mapped["User"] = orm.relationship(back_populates="transactions")
    categories: orm.Mapped[list["Category"]] = orm.relationship(
        back_populates="transactions",
        secondary="transactions_categories",
    )

import typing as tp
from datetime import datetime

from sqlalchemy import orm, types, schema

from . import base, mixins

if tp.TYPE_CHECKING:
    from .user import User
    from .category import Category

__all__ = ["Budget"]


class Budget(mixins.CreatedAtMixin, mixins.PrimaryKeyIDMixin, base.Base):
    user_id: orm.Mapped[int] = orm.mapped_column(schema.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    amount: orm.Mapped[float] = orm.mapped_column(types.Numeric(10, 2), nullable=False)
    start_date: orm.Mapped[datetime] = orm.mapped_column(types.DateTime(timezone=True), nullable=False)
    end_date: orm.Mapped[datetime] = orm.mapped_column(types.DateTime(timezone=True), nullable=False)

    user: orm.Mapped["User"] = orm.relationship(back_populates="budgets")
    categories: orm.Mapped[list["Category"]] = orm.relationship(
        back_populates="budget",
        foreign_keys="[Category.budget_id, Category.user_id]",
        overlaps="categories,children,parent,user",
    )

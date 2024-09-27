import typing as tp

from sqlalchemy import orm, types, schema

from . import base, mixins

if tp.TYPE_CHECKING:
    from .transaction import Transaction
    from .user import User
    from .budget import Budget

__all__ = ["Category"]


class Category(mixins.PrimaryKeyIDMixin, base.Base):
    __tablename__ = "categories"  # type: ignore
    __table_args__ = (
        schema.ForeignKeyConstraint(
            ["parent_id", "user_id"],
            ["categories.id", "categories.user_id"],
            ondelete="SET NULL",
        ),
        schema.ForeignKeyConstraint(
            ["budget_id", "user_id"],
            ["budgets.id", "budgets.user_id"],
            ondelete="SET NULL",
        ),
    )

    user_id: orm.Mapped[int] = orm.mapped_column(schema.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    title: orm.Mapped[str] = orm.mapped_column(types.String(64), nullable=False)
    budget_id: orm.Mapped[tp.Optional[int]] = orm.mapped_column(types.BigInteger, nullable=True)
    parent_id: orm.Mapped[tp.Optional[int]] = orm.mapped_column(types.BigInteger, nullable=True)

    budget: orm.Mapped[tp.Optional["Budget"]] = orm.relationship(
        back_populates="categories", foreign_keys="[Category.budget_id, Category.user_id]", overlaps="categories"
    )
    parent: orm.Mapped[tp.Optional["Category"]] = orm.relationship(
        back_populates="children",
        foreign_keys="[Category.parent_id, Category.user_id]",
        remote_side="[Category.id, Category.user_id]",
        overlaps="budget,categories",
    )
    children: orm.Mapped[list["Category"]] = orm.relationship(
        back_populates="parent",
        foreign_keys="[Category.parent_id, Category.user_id]",
        remote_side="[Category.parent_id, Category.user_id]",
        overlaps="budget,categories",
    )
    user: orm.Mapped["User"] = orm.relationship(back_populates="categories", overlaps="budget,children,parent")
    transactions: orm.Mapped[list["Transaction"]] = orm.relationship(
        back_populates="categories",
        secondary="transactions_categories",
    )

import typing as tp

from sqlalchemy import orm, schema, types

from . import base, mixins

if tp.TYPE_CHECKING:
    pass

__all__ = ["TransactionCategory"]


class TransactionCategory(mixins.CreatedAtMixin, base.Base):
    __tablename__ = "transactions_categories"  # type: ignore
    __table_args__ = (
        schema.ForeignKeyConstraint(
            ["user_id", "transaction_id"],
            ["transactions.user_id", "transactions.id"],
            ondelete="CASCADE",
        ),
        schema.ForeignKeyConstraint(
            ["user_id", "category_id"],
            ["categories.user_id", "categories.id"],
            ondelete="CASCADE",
        ),
    )

    user_id: orm.Mapped[int] = orm.mapped_column(schema.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    transaction_id: orm.Mapped[int] = orm.mapped_column(types.BigInteger, primary_key=True)
    category_id: orm.Mapped[int] = orm.mapped_column(types.BigInteger, primary_key=True)

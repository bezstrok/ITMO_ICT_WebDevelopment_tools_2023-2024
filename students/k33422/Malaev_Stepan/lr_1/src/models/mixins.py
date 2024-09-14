from sqlalchemy import orm, types, sql

__all__ = ["PrimaryKeyIDMixin"]


class PrimaryKeyIDMixin:
    id: orm.Mapped[int] = orm.mapped_column(types.BigInteger, primary_key=True, autoincrement=True)


class CreatedAtMixin:
    created_at: orm.Mapped[str] = orm.mapped_column(
        types.DateTime(timezone=True), server_default=sql.func.now(), nullable=True
    )

from sqlalchemy import orm, schema
from sqlalchemy.ext.asyncio import AsyncAttrs

from ..services.string import Format
from .mixins import RepositoryMixin

__all__ = ["Base"]


class Base(RepositoryMixin, AsyncAttrs, orm.DeclarativeBase):
    __abstract__ = True

    metadata = schema.MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )

    @orm.declared_attr.directive
    def __tablename__(cls) -> str:  # noqa
        return f"{Format.snake_case(cls.__name__)}s"

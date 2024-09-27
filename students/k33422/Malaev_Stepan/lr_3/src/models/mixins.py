import typing as tp

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import LoaderOption
from sqlalchemy import orm, types, sql

from ..services.database import Database
from ..services.repository import Repository

if tp.TYPE_CHECKING:
    from .base import Base  # type: ignore
else:

    class Base:
        pass


__all__ = ["PrimaryKeyIDMixin", "CreatedAtMixin", "RepositoryMixin"]

Mapping = tp.Mapping[str, tp.Any]


class PrimaryKeyIDMixin:
    id: orm.Mapped[int] = orm.mapped_column(types.BigInteger, primary_key=True, autoincrement=True)


class CreatedAtMixin:
    created_at: orm.Mapped[str] = orm.mapped_column(
        types.DateTime(timezone=True), server_default=sql.func.now(), nullable=True
    )


class RepositoryMixin(Base):  # type: ignore
    @classmethod
    @Database.with_session
    async def create_one(
        cls,
        data: Mapping,
        *,
        result: bool = False,
        session: AsyncSession,
    ) -> tp.Optional[tp.Self]:
        instance = cls(**data)

        session.add(instance)

        if result:
            await session.flush()
            await session.refresh(instance)
            return instance

        return None

    @classmethod
    @Database.with_session
    async def create_many(
        cls,
        data: tp.Sequence[Mapping],
        *,
        result: bool = False,
        session: AsyncSession,
    ) -> tp.Optional[list[tp.Self]]:
        instances = [cls(**d) for d in data]

        session.add_all(instances)

        if result:
            await session.flush()
            for instance in instances:
                await session.refresh(instance)
            return instances

        return None

    @classmethod
    @Database.with_session
    async def update_one(
        cls,
        data: Mapping,
        filters: Mapping,
        *,
        result: bool = False,
        session: AsyncSession,
    ) -> tp.Optional[tp.Self]:
        statement = sql.update(cls).values(data).where(*Repository.build_django_filters(cls, filters))
        if result:
            statement = statement.returning(cls)

        execution = await session.execute(statement)

        if result:
            return tp.cast(tp.Self, execution.scalar_one())

        return None

    @classmethod
    @Database.with_session
    async def update_many(
        cls,
        data: Mapping,
        filters: Mapping,
        *,
        result: bool = False,
        session: AsyncSession,
    ) -> tp.Optional[list[tp.Self]]:
        statement = sql.update(cls).values(data).where(*Repository.build_django_filters(cls, filters))
        if result:
            statement = statement.returning(cls)

        execution = await session.execute(statement)

        if result:
            return list(execution.scalars().all())

        return None

    @Database.with_session
    async def update_self(
        self,
        data: Mapping,
        *,
        result: bool = False,
        session: AsyncSession,
    ) -> tp.Optional[tp.Self]:
        for attr, value in data.items():
            setattr(self, attr, value)

        session.add(self)

        if result:
            await session.flush()
            await session.refresh(self)
            return self

        return None

    @classmethod
    @Database.with_session
    async def delete_one(
        cls,
        filters: Mapping,
        *,
        result: bool = False,
        session: AsyncSession,
    ) -> tp.Optional[tp.Self]:
        statement = sql.delete(cls).where(*Repository.build_django_filters(cls, filters))
        if result:
            statement = statement.returning(cls)  # type: ignore

        execution = await session.execute(statement)

        if result:
            return tp.cast(tp.Self, execution.scalar_one())

        return None

    @classmethod
    @Database.with_session
    async def delete_many(
        cls,
        filters: Mapping,
        *,
        result: bool = False,
        session: AsyncSession,
    ) -> tp.Optional[list[tp.Self]]:
        statement = sql.delete(cls).where(*Repository.build_django_filters(cls, filters))
        if result:
            statement = statement.returning(cls)  # type: ignore

        execution = await session.execute(statement)

        if result:
            return list(execution.scalars().all())

        return None

    @Database.with_session
    async def delete_self(
        self,
        *,
        result: bool = False,
        session: AsyncSession,
    ) -> tp.Optional[tp.Self]:
        await session.delete(self)

        if result:
            await session.flush()
            return self

        return None

    @classmethod
    @Database.with_session
    async def get_one(
        cls,
        filters: Mapping,
        *,
        fields: tp.Optional[tp.Sequence[str]] = None,
        loads: tp.Optional[tp.Sequence[LoaderOption]] = None,
        session: AsyncSession,
    ) -> tp.Optional[tp.Self]:
        entities: list[tp.Any]
        if fields is None:
            entities = [cls]
        else:
            entities = Repository.build_fields(cls, fields)

        statement = sql.select(*entities).where(*Repository.build_django_filters(cls, filters))

        if loads is not None:
            statement = statement.options(*loads)

        execution = await session.execute(statement)

        return execution.scalar_one_or_none()

    @classmethod
    @Database.with_session
    async def get_many(
        cls,
        filters: Mapping,
        *,
        fields: tp.Optional[tp.Sequence[str]] = None,
        loads: tp.Optional[tp.Sequence[LoaderOption]] = None,
        orders: tp.Optional[tp.Sequence[str]] = None,
        limit: tp.Optional[int] = None,
        offset: tp.Optional[int] = None,
        distinct: bool = False,
        session: AsyncSession,
    ) -> list[tp.Self]:
        entities: list[tp.Any]
        if fields is None:
            entities = [cls]
        else:
            entities = Repository.build_fields(cls, fields)
        if orders is None:
            orders = []

        statement = (
            sql.select(*entities)
            .where(*Repository.build_django_filters(cls, filters))
            .order_by(*Repository.build_django_orders(cls, orders))
        )

        if loads is not None:
            statement = statement.options(*loads)
        if distinct:
            statement = statement.distinct()
        if limit is not None:
            statement = statement.limit(limit)
        if offset is not None:
            statement = statement.offset(offset)

        execution = await session.execute(statement)

        return list(execution.scalars().all())

    @classmethod
    @Database.with_session
    async def count(
        cls,
        filters: Mapping,
        *,
        session: AsyncSession,
    ) -> int:
        statement = sql.select(sql.func.count()).where(*Repository.build_django_filters(cls, filters))

        execution = await session.execute(statement)

        return execution.scalar_one()

    @classmethod
    @Database.with_session
    async def exists(
        cls,
        filters: Mapping,
        *,
        session: AsyncSession,
    ) -> bool:
        statement = sql.select(sql.exists().where(*Repository.build_django_filters(cls, filters)))

        execution = await session.execute(statement)

        return execution.scalar_one()

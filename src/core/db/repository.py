from sqlalchemy import insert, select, Select

from .db import get_async_session_maker, get_sync_session_maker

from abc import abstractmethod, ABC
from typing import Generic, TypeVar, TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession


MODEL = TypeVar('MODEL')


class AbstractRepository(ABC, Generic[MODEL]):
    @abstractmethod
    async def create(self, session: 'AsyncSession') -> MODEL:
        raise NotImplementedError

    @abstractmethod
    async def find_all(self, *filters, **filter_by) -> MODEL:
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, *filters, **filter_by) -> MODEL:
        raise NotImplementedError

    @abstractmethod
    async def exists(self, *filers, **filter_by) -> MODEL:
        raise NotImplementedError

    @abstractmethod
    async def save(self, instance: MODEL) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, instance: MODEL) -> None:
        raise NotImplementedError

    @abstractmethod
    def build_statement(
        self, *filters, order: str = 'id', limit: int = None, offset: int = None, **filter_by,
    ) -> Select:
        raise NotImplementedError


class BaseSQLAlchemyRepository(AbstractRepository[MODEL], ABC):
    model: MODEL = None

    def build_statement(
        self,
        *filters,
        order: str = 'id',
        limit: int = None,
        offset: int = None,
        options: str = None,
        **filter_by,
    ) -> Select:
        statement = select(self.model)

        if filters:
            statement = statement.filter(*filters)
        elif filter_by:
            statement = statement.filter_by(**filter_by)

        if order is not None:
            statement = statement.order_by(order)
        if limit is not None:
            statement = statement.limit(limit)
        if offset is not None:
            statement = statement.offset(offset)
        if options is not None:
            statement = statement.options(options)

        return statement


class SyncSQLAlchemyRepository(BaseSQLAlchemyRepository[MODEL]):
    def create(self, **data) -> MODEL:
        with get_sync_session_maker() as session:
            statement = insert(self.model).values(**data).returning(self.model)

            result = session.execute(statement)
            session.commit()

            return result.scalar_one()

    def find_one(self, *filters, **filter_by) -> MODEL:
        results = self.find_all(*filters, **filter_by)

        if len(results) > 0:
            return results[0]

        return None

    def find_all(self, *filters, **filter_by) -> list[MODEL]:
        with get_sync_session_maker() as session:
            statement = self.build_statement(*filters, **filter_by)

            result = session.execute(statement)

            return list(map(lambda x: x[0], result.all()))

    def exists(self, *filters, **filter_by) -> bool:
        with get_sync_session_maker() as session:
            statement = self.build_statement(*filters, **filter_by)

            result = session.execute(statement)

            return result.scalar_one_or_none() is not None

    def save(self, instance: MODEL) -> None:
        with get_sync_session_maker() as session:
            session.add(instance)
            session.commit()

    def delete(self, instance: MODEL) -> None:

        with get_sync_session_maker() as session:
            session.delete(instance)
            session.commit()


class SQLAlchemyRepository(SyncSQLAlchemyRepository[MODEL]):
    def __new__(cls, *args, **kwargs):
        is_sync = kwargs.get('sync', False)

        if is_sync is True:
            sync_repository = SyncSQLAlchemyRepository()
            sync_repository.model = cls.model
            return sync_repository

        return super(SQLAlchemyRepository, cls).__new__(cls)

    async def create(self, **data) -> MODEL:
        async with get_async_session_maker() as session:
            statement = insert(self.model).values(**data).returning(self.model)
            result = await session.execute(statement)
            await session.commit()

            return result.scalar_one()

    async def find_one(self, *filters, **filter_by) -> MODEL:
        results = await self.find_all(*filters, **filter_by)

        if len(results) > 0:
            return results[0]

        return None

    async def find_all(self, *filters, order_by = None, **filter_by) -> list[MODEL]:
        async with get_async_session_maker() as session:
            statement = self.build_statement(*filters, **filter_by)
            result = await session.execute(statement)

            return list(map(lambda x: x[0], result.all()))

    async def exists(self, *filters, **filter_by) -> bool:
        async with get_async_session_maker() as session:
            statement = self.build_statement(*filters, **filter_by)

            result = await session.execute(statement)

            return result.scalar() is not None

    async def save(self, instance: MODEL) -> None:
        async with get_async_session_maker() as session:
            session.add(instance)
            await session.commit()

    async def delete(self, instance: MODEL) -> None:
        async with get_async_session_maker() as session:
            await session.delete(instance)
            await session.commit()

__all__ = (
    'SQLAlchemyRepository',
)

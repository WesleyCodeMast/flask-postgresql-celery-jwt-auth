from sqlalchemy import create_engine as create_sync_engine
from sqlalchemy.orm import sessionmaker as sync_sessionmaker, close_all_sessions as sync_close_all_sessions

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, \
    close_all_sessions as async_close_all_sessions

from loguru import logger

from sqlalchemy import Engine as SyncEngine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from core.settings import Settings


_db_async_engine: 'AsyncEngine'
_db_async_session_maker: async_sessionmaker

_db_sync_engine: 'SyncEngine'
_db_sync_session_maker: sync_sessionmaker


async def get_async_db_session() -> 'AsyncSession':
    async with _db_async_session_maker() as session:
        yield session


def get_async_session_maker() -> async_sessionmaker:
    return _db_async_session_maker()


async def setup_database_service(settings: 'Settings') -> None:
    global _db_async_engine, _db_async_session_maker

    _db_async_engine = create_async_engine(str(settings.DATABASE_URL))
    _db_async_session_maker = async_sessionmaker(_db_async_engine, expire_on_commit=False)

    from sqlalchemy import text

    async with _db_async_session_maker() as session:
        statement = text('SELECT 1')
        await session.execute(statement)

    logger.debug('setup_database_service() attached')


async def shutdown_database_service() -> None:
    await async_close_all_sessions()
    await _db_async_engine.dispose()


def get_sync_session_maker() -> sync_sessionmaker:
    return _db_sync_session_maker()


def setup_database_service_sync(settings: 'Settings') -> None:
    global _db_sync_engine, _db_sync_session_maker

    database_url = str(settings.DATABASE_URL).replace('asyncpg', 'psycopg2')

    _db_sync_engine = create_sync_engine(database_url)
    _db_sync_session_maker = sync_sessionmaker(_db_sync_engine, expire_on_commit=False)


def shutdown_database_service_sync() -> None:
    sync_close_all_sessions()
    _db_sync_engine.dispose()


__all__ = (
    'get_async_db_session',
    'get_async_session_maker',
    'setup_database_service',
    'shutdown_database_service',
    'get_sync_session_maker',
    'setup_database_service_sync',
    'shutdown_database_service_sync',
)

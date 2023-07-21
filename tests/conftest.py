import asyncio
import pytest
import pytest_asyncio
from typing import Iterator
from fastapi import FastAPI
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession, async_sessionmaker
from fastapi.testclient import TestClient

from project.infrastructure.models import Base
from project.presentation.api import router


@pytest.fixture(scope="session")
def event_loop() -> Iterator[asyncio.AbstractEventLoop]:
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


# https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#serializable-isolation-savepoints-transactional-ddl
def do_connect(dbapi_connection, connection_record):
    # disable pysqlite's emitting of the BEGIN statement entirely.
    # also stops it from emitting COMMIT before any DDL.
    dbapi_connection.isolation_level = None


def do_begin(conn):
    # emit our own BEGIN
    conn.exec_driver_sql("BEGIN")


@pytest_asyncio.fixture(scope='session')
async def engine() -> AsyncEngine:
    engine = create_async_engine('sqlite+aiosqlite://',
                                 connect_args={'check_same_thread': False},
                                 echo=True,
                                 echo_pool="debug"
                                 )

    event.listen(engine.sync_engine, "connect", do_connect)
    event.listen(engine.sync_engine, "begin", do_begin)
    return engine


@pytest_asyncio.fixture(autouse=True, scope='session')
async def db(engine: AsyncEngine):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


@pytest.fixture(scope='session')
def app() -> FastAPI:
    test_app = FastAPI()
    test_app.include_router(router)
    return test_app


@pytest_asyncio.fixture(scope="function")
async def session(engine: AsyncEngine) -> AsyncSession:
    """
    From the doc: https://tinyurl.com/mwhv5b9y
    """
    async with engine.connect() as connection:
        async with connection.begin():
            session_factory = async_sessionmaker()
            session = session_factory(bind=connection, join_transaction_mode="create_savepoint")
            yield session
            await session.close()


@pytest.fixture
def client(app) -> TestClient:
    test_client = TestClient(app)
    return test_client

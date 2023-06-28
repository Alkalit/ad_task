import pytest
from fastapi import FastAPI
from sqlalchemy import create_engine, Engine, event
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient

from project.infrastructure.models import Base
from project.presentation.api import router


# https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#serializable-isolation-savepoints-transactional-ddl
def do_connect(dbapi_connection, connection_record):
    # disable pysqlite's emitting of the BEGIN statement entirely.
    # also stops it from emitting COMMIT before any DDL.
    dbapi_connection.isolation_level = None


def do_begin(conn):
    # emit our own BEGIN
    conn.exec_driver_sql("BEGIN")


@pytest.fixture(scope='session')
def engine() -> Engine:
    engine = create_engine('sqlite://',
                           connect_args={'check_same_thread': False},
                           echo=True,
                           echo_pool="debug"
                           )

    event.listen(engine, "connect", do_connect)
    event.listen(engine, "begin", do_begin)

    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(scope='session')
def app() -> FastAPI:
    test_app = FastAPI()
    test_app.include_router(router)
    return test_app


@pytest.fixture
def session(engine: Engine) -> Session:
    """
    From the doc: https://tinyurl.com/mwhv5b9y
    """
    connection = engine.connect()
    transaction = connection.begin()

    session_factory = sessionmaker()
    session = session_factory(bind=connection, join_transaction_mode="create_savepoint")
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(app) -> TestClient:
    test_client = TestClient(app)
    return test_client

import pytest
from fastapi import FastAPI
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient

from database import Base
from api import router


@pytest.fixture(scope='session')
def engine() -> Engine:
    engine = create_engine("sqlite:///:memory:", connect_args=dict(check_same_thread=False))
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

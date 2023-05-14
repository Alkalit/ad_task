import pytest
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

from database import Base


@pytest.fixture(scope='session')
def db() -> Engine:
    engine = create_engine(":memory:")
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture
def session(db: Engine) -> Session:
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=db)
    return session_factory()

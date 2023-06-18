from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
Base = declarative_base()


def setup_engine() -> Engine:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=dict(check_same_thread=False))
    return engine


def setup_session(engine) -> sessionmaker:
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return session_factory

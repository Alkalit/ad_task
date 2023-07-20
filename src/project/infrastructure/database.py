from pathlib import Path
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine

import project

project_dir = Path(project.__file__).parent.parent.parent
db_path = project_dir / 'app.sqlite3'

SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"


def setup_engine() -> Engine:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args=dict(check_same_thread=False),
    )
    return engine


def setup_session(engine) -> sessionmaker:
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return session_factory


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode = DELETE")
    cursor.close()

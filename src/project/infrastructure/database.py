from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession
from sqlalchemy.engine import Engine
from sqlalchemy import event

import project

project_dir = Path(project.__file__).parent.parent.parent
db_path = project_dir / 'app.sqlite3'

SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///{db_path}"


def setup_engine() -> AsyncEngine:
    engine = create_async_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args=dict(check_same_thread=False),
    )
    return engine


def setup_session(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    session_factory = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return session_factory


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")  # default DELETE
    cursor.close()

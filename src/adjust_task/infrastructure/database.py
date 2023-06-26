from pathlib import Path
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker

this_file = Path(__file__)
project_dir = this_file.parent.parent.parent.parent
db_path = project_dir / 'app.sqlite3'

SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"


def setup_engine() -> Engine:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args=dict(check_same_thread=False),
        echo=True,
        echo_pool="debug",
    )
    return engine


def setup_session(engine) -> sessionmaker:
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return session_factory

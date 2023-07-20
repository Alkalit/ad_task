from asyncio import run
from sqlalchemy.ext.asyncio import AsyncSession

from project.infrastructure.framework import setup_api
from project.infrastructure.database import setup_engine, setup_session


def main() -> None:
    engine = setup_engine()
    session_factory = setup_session(engine)

    app = setup_api()
    app.dependency_overrides[AsyncSession] = lambda: session_factory()
    return app
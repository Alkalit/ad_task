from typing import AsyncGenerator, Callable
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI

from project.infrastructure.framework import setup_api
from project.infrastructure.database import setup_engine, setup_session


def session_manager(
        session_factory: Callable[[], AsyncSession]
) -> Callable[[], AsyncGenerator[AsyncSession, None]]:

    async def wrapper() -> AsyncGenerator[AsyncSession, None]:
        session = session_factory()
        yield session
        await session.close()
    return wrapper


def main() -> FastAPI:
    engine = setup_engine()
    session_factory = setup_session(engine)

    app = setup_api()
    app.dependency_overrides[AsyncSession] = session_manager(session_factory)
    return app

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI

from project.infrastructure.framework import setup_api
from project.infrastructure.database import setup_engine, setup_session

# def session_manager(session_factory: Callable[[], AsyncSession])


def main() -> FastAPI:
    engine = setup_engine()
    session_factory = setup_session(engine)

    async def session_manager() -> AsyncGenerator[AsyncSession, None]:
        session = session_factory()
        yield session
        await session.close()

    app = setup_api()
    # app.dependency_overrides[AsyncSession] = lambda: session_factory()
    app.dependency_overrides[AsyncSession] = session_manager
    return app

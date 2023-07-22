from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI

from project.infrastructure.framework import setup_api, session_manager
from project.infrastructure.database import setup_engine, setup_session


def main() -> FastAPI:
    engine = setup_engine()
    session_factory = setup_session(engine)

    app = setup_api()
    app.dependency_overrides[AsyncSession] = session_manager(session_factory)
    return app

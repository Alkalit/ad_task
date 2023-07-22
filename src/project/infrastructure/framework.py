from typing import Callable, AsyncGenerator

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from project.presentation.api import router


def setup_app(app: FastAPI) -> None:
    app.include_router(router)


def setup_api() -> FastAPI:
    app = FastAPI()
    setup_app(app)

    return app


def session_manager(
        session_factory: Callable[[], AsyncSession]
) -> Callable[[], AsyncGenerator[AsyncSession, None]]:
    async def wrapper() -> AsyncGenerator[AsyncSession, None]:
        session = session_factory()
        yield session
        await session.close()

    return wrapper

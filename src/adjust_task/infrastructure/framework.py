from fastapi import FastAPI

from adjust_task.presentation.api import router


def setup_app(app: FastAPI) -> None:
    app.include_router(router)


def setup_api() -> FastAPI:
    app = FastAPI()
    setup_app(app)

    return app

import uvicorn
from fastapi import FastAPI
from sqlalchemy.orm import Session

from api import router
from database import Base, setup_engine, setup_session


def setup_app(app: FastAPI) -> None:
    app.include_router(router)


def run_server(app: FastAPI) -> None:
    uvicorn_config = uvicorn.Config(app)
    server = uvicorn.Server(uvicorn_config)
    server.run()


def setup_api() -> FastAPI:
    app = FastAPI()
    setup_app(app)

    return app


def main() -> None:
    engine = setup_engine()
    session_factory = setup_session(engine)
    Base.metadata.create_all(bind=engine)

    app = setup_api(session_factory)
    app.dependency_overrides[Session] = lambda: session_factory()

    return run_server(app)


if __name__ == '__main__':
    main()

import uvicorn
from fastapi import FastAPI
from sqlalchemy.orm import Session

from api import router
from database import Base, engine, SessionFactory


def setup_fastapi() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[Session] = lambda: SessionFactory()
    return app


def run_server(app: FastAPI) -> None:
    uvicorn_config = uvicorn.Config(app)
    server = uvicorn.Server(uvicorn_config)
    server.run()


def main() -> None:
    Base.metadata.create_all(bind=engine)
    app = setup_fastapi()
    return run_server(app)


if __name__ == '__main__':
    main()

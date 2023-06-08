from fastapi import FastAPI
from sqlalchemy.orm import Session

from api import router
from database import Base, engine, SessionFactory


def setup_fastapi() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app

app = setup_fastapi()

app.dependency_overrides[Session] = lambda: SessionFactory()

Base.metadata.create_all(bind=engine)

from fastapi import FastAPI
from database import Base, engine, SessionFactory
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, Engine

from services import AnalyticsService, BaseAnalyticsService

from api import router


def setup_fastapi() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    service = AnalyticsService()
    app.dependency_overrides[BaseAnalyticsService] = lambda: service
    return app

app = setup_fastapi()

app.dependency_overrides[Session] = lambda: SessionFactory()

Base.metadata.create_all(bind=engine)

from fastapi import FastAPI
from database import Base, engine, SessionFactory
from sqlalchemy.orm import Session

from api import router

app = FastAPI()
app.include_router(router)

Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    app.dependency_overrides[Session] = SessionFactory

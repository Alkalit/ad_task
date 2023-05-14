from fastapi import FastAPI
from database import Base, engine

from api import router

app = FastAPI()
app.include_router(router)

Base.metadata.create_all(bind=engine)

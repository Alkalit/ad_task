import uvicorn
from fastapi import FastAPI


def run_server(app: FastAPI) -> None:
    uvicorn_config = uvicorn.Config(app)
    server = uvicorn.Server(uvicorn_config)
    server.run()

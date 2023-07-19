import uvicorn
from fastapi import FastAPI


async def run_server(app: FastAPI) -> None:
    uvicorn_config = uvicorn.Config(app, workers=8)
    server = uvicorn.Server(uvicorn_config)
    await server.serve()

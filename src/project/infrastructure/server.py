import uvicorn
from fastapi import FastAPI


async def run_server(app: FastAPI) -> None:
    """
    Manual launch of a uvicorn instance. May be used in case of deployment in containers.
    https://fastapi.tiangolo.com/deployment/docker/#docker-compose
    """
    uvicorn_config = uvicorn.Config(app)
    server = uvicorn.Server(uvicorn_config)
    await server.serve()

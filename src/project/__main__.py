from asyncio import run
from sqlalchemy.orm import Session

from project.infrastructure.framework import setup_api
from project.infrastructure.database import setup_engine, setup_session
from project.infrastructure.server import run_server


async def main() -> None:
    engine = setup_engine()
    session_factory = setup_session(engine)

    app = setup_api()
    app.dependency_overrides[Session] = lambda: session_factory()  # TODO async

    await run_server(app)


if __name__ == '__main__':
    run(main())

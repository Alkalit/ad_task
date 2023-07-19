from sqlalchemy.orm import Session

from project.infrastructure.framework import setup_api
from project.infrastructure.database import setup_engine, setup_session
from project.infrastructure.server import run_server


def main():
    engine = setup_engine()
    session_factory = setup_session(engine)

    app = setup_api()
    app.dependency_overrides[Session] = lambda: session_factory()

    return app
    # return run_server(app)

app = main()
# if __name__ == '__main__':
#     main()

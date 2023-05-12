from fastapi.testclient import TestClient
from httpx import Response

from main import app


class TestRootEndpoint:

    def test_root_if_no_ads(self):
        client = TestClient(app)
        response: Response = client.get("/")
        assert response.json() == []

    def test_if_ads(self):
        pass

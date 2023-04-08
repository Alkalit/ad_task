from httpx import Response
from fastapi import FastAPI
from fastapi.testclient import TestClient


app = FastAPI()


class TestRootEndpoint:

    def test_root_if_no_ads(self):
        client = TestClient(app)
        response: Response = client.get("/")
        assert response.json() == []

    def test_if_ads(self):
        pass

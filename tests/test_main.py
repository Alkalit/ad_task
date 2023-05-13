from fastapi.testclient import TestClient
from httpx import Response

from main import app


class TestRootEndpoint:

    def test_root_if_no_ads(self):
        client = TestClient(app)
        response: Response = client.get("/")
        assert response.json() == []

    def test_if_ads(self):
        client = TestClient(app)
        response: Response = client.get("/")
        assert response.json() == [
            {"date": "2017-05-17", "channel": "adcolony", "country": "US", "os": "android", "impressions": 1000,
             "clicks": 100, "installs": 10, "spend": 11.1, "revenue": 111.1},
            {"date": "2017-05-17", "channel": "adcolony", "country": "US", "os": "ios", "impressions": 2000,
             "clicks": 200, "installs": 20, "spend": 22.2, "revenue": 222.2},
            {"date": "2017-05-17", "channel": "apple_search_ads", "country": "DE", "os": "ios", "impressions": 3000,
             "clicks": 300, "installs": 30, "spend": 33.3, "revenue": 333.3},
        ]

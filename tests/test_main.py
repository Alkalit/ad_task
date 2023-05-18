import pytest
from fastapi.testclient import TestClient
from httpx import Response
from sqlalchemy.orm import Session

from db_models import CampaignStat
from decimal import Decimal
from datetime import date


@pytest.fixture(autouse=True)
def session_override(app, session):
    app.dependency_overrides[Session] = lambda: session


class TestRootEndpoint:

    def test_root_if_no_ads(self, client: TestClient):
        response: Response = client.get("/")
        assert response.json() == []

    def test_if_ads(self, client: TestClient, session: Session):
        session.add(CampaignStat(
            date=date(year=2017, month=5, day=17),
            channel='adcolony',
            country='US',
            os='android',
            impressions=1000,
            clicks=100,
            installs=10,
            spend=Decimal('11.1'),
            revenue=Decimal('111.1')
        ))
        session.add(CampaignStat(
            date=date(year=2017, month=5, day=17),
            channel='adcolony',
            country='US',
            os='ios',
            impressions=2000,
            clicks=200,
            installs=20,
            spend=Decimal('22.2'),
            revenue=Decimal('222.2')
        ))
        session.add(CampaignStat(
            date=date(year=2017, month=5, day=17),
            channel='apple_search_ads',
            country='DE',
            os='ios',
            impressions=3000,
            clicks=300,
            installs=30,
            spend=Decimal('33.3'),
            revenue=Decimal('333.3')
        ))
        session.commit()

        response: Response = client.get("/")
        assert response.json() == [
            {"date": "2017-05-17", "channel": "adcolony", "country": "US", "os": "android", "impressions": 1000,
             "clicks": 100, "installs": 10, "spend": 11.1, "revenue": 111.1},
            {"date": "2017-05-17", "channel": "adcolony", "country": "US", "os": "ios", "impressions": 2000,
             "clicks": 200, "installs": 20, "spend": 22.2, "revenue": 222.2},
            {"date": "2017-05-17", "channel": "apple_search_ads", "country": "DE", "os": "ios", "impressions": 3000,
             "clicks": 300, "installs": 30, "spend": 33.3, "revenue": 333.3},
        ]

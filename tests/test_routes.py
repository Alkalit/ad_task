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


@pytest.fixture
def data_sample(session: Session) -> tuple[CampaignStat]:
    stat1 = CampaignStat(
        date=date(year=2001, month=1, day=1),
        channel='adcolony',
        country='US',
        os='android',
        impressions=1000,
        clicks=100,
        installs=10,
        spend=Decimal('11.1'),
        revenue=Decimal('111.1')
    )
    stat2 = CampaignStat(
        date=date(year=2002, month=2, day=2),
        channel='betcolony',
        country='US',
        os='ios',
        impressions=2000,
        clicks=200,
        installs=20,
        spend=Decimal('22.2'),
        revenue=Decimal('222.2')
    )
    stat3 = CampaignStat(
        date=date(year=2003, month=3, day=3),
        channel='cedcolony',
        country='DE',
        os='ios',
        impressions=3000,
        clicks=300,
        installs=30,
        spend=Decimal('33.3'),
        revenue=Decimal('333.3')
    )
    session.add(stat1)
    session.add(stat2)
    session.add(stat3)
    session.commit()
    return (stat1, stat2, stat3)


class TestRootEndpoint:

    def test_root_if_no_ads(self, client: TestClient):
        response: Response = client.get("/")
        assert response.json() == []

    def test_if_ads(self, client: TestClient, data_sample: tuple[CampaignStat]):

        response: Response = client.get("/")
        assert response.json() == [
            {"date": "2001-01-01", "channel": "adcolony", "country": "US", "os": "android", "impressions": 1000,
             "clicks": 100, "installs": 10, "spend": 11.1, "revenue": 111.1},
            {"date": "2002-02-02", "channel": "betcolony", "country": "US", "os": "ios", "impressions": 2000,
             "clicks": 200, "installs": 20, "spend": 22.2, "revenue": 222.2},
            {"date": "2003-03-03", "channel": "cedcolony", "country": "DE", "os": "ios", "impressions": 3000,
             "clicks": 300, "installs": 30, "spend": 33.3, "revenue": 333.3},
        ]

    def test_filters_date_from(self, client: TestClient, data_sample: tuple[CampaignStat]):
        response: Response = client.get("/?date_from=2001-02-01")

    def test_filters_date_to(self, client: TestClient, data_sample: tuple[CampaignStat]):
        response: Response = client.get("/?date_to=2001-02-01")

    def test_filters_channels(self, client: TestClient, data_sample: tuple[CampaignStat]):
        response: Response = client.get("/?channel=adcolony")

    def test_filters_countries(self, client: TestClient, data_sample: tuple[CampaignStat]):
        response: Response = client.get("/?country=us")

    def test_filters_oses(self, client: TestClient, data_sample: tuple[CampaignStat]):
        response: Response = client.get("/?os=android")

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
        country='RU',
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
        os='windows',
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


@pytest.fixture
def groupby_dataset(session: Session):
    stats = [
        CampaignStat(
            date=date(year=2001, month=1, day=1),
            channel='adcolony',
            country='RU',
            os='android',
            impressions=1000,
            clicks=100,
            installs=10,
            spend=Decimal('11.1'),
            revenue=Decimal('111.1')
        ),
        CampaignStat(
            date=date(year=2001, month=1, day=1),
            channel='adcolony',
            country='RU',
            os='android',
            impressions=1000,
            clicks=100,
            installs=10,
            spend=Decimal('11.1'),
            revenue=Decimal('111.1')
        ),
        CampaignStat(
            date=date(year=2001, month=1, day=1),
            channel='adcolony',
            country='RU',
            os='android',
            impressions=1000,
            clicks=100,
            installs=10,
            spend=Decimal('11.1'),
            revenue=Decimal('111.1')
        ),

        CampaignStat(
            date=date(year=2002, month=2, day=2),
            channel='betcolony',
            country='US',
            os='ios',
            impressions=2000,
            clicks=200,
            installs=20,
            spend=Decimal('22.2'),
            revenue=Decimal('222.2')
        ),
        CampaignStat(
            date=date(year=2002, month=2, day=2),
            channel='betcolony',
            country='US',
            os='ios',
            impressions=2000,
            clicks=200,
            installs=20,
            spend=Decimal('22.2'),
            revenue=Decimal('222.2')
        ),
        CampaignStat(
            date=date(year=2002, month=2, day=2),
            channel='betcolony',
            country='US',
            os='ios',
            impressions=2000,
            clicks=200,
            installs=20,
            spend=Decimal('22.2'),
            revenue=Decimal('222.2')
        ),

        CampaignStat(
            date=date(year=2003, month=3, day=3),
            channel='cedcolony',
            country='DE',
            os='windows',
            impressions=3000,
            clicks=300,
            installs=30,
            spend=Decimal('33.3'),
            revenue=Decimal('333.3')
        ),
        CampaignStat(
            date=date(year=2003, month=3, day=3),
            channel='cedcolony',
            country='DE',
            os='windows',
            impressions=3000,
            clicks=300,
            installs=30,
            spend=Decimal('33.3'),
            revenue=Decimal('333.3')
        ),
        CampaignStat(
            date=date(year=2003, month=3, day=3),
            channel='cedcolony',
            country='DE',
            os='windows',
            impressions=3000,
            clicks=300,
            installs=30,
            spend=Decimal('33.3'),
            revenue=Decimal('333.3')
        ),
    ]
    session.bulk_save_objects(stats)


class TestRootEndpoint:

    def test_root_if_no_ads(self, client: TestClient):
        response: Response = client.get("/")
        assert response.status_code == 200
        assert response.json() == []

    def test_if_ads(self, client: TestClient, data_sample: tuple[CampaignStat]):
        response: Response = client.get("/")
        assert response.status_code == 200
        assert response.json() == [
            {"date": "2001-01-01", "channel": "adcolony", "country": "RU", "os": "android", "impressions": 1000,
             "clicks": 100, "installs": 10, "spend": 11.1, "revenue": 111.1, "cpi": 1.11},
            {"date": "2002-02-02", "channel": "betcolony", "country": "US", "os": "ios", "impressions": 2000,
             "clicks": 200, "installs": 20, "spend": 22.2, "revenue": 222.2, "cpi": 1.11},
            {"date": "2003-03-03", "channel": "cedcolony", "country": "DE", "os": "windows", "impressions": 3000,
             "clicks": 300, "installs": 30, "spend": 33.3, "revenue": 333.3, "cpi": 1.11},
        ]

    def test_filters_date_from(self, client: TestClient, data_sample: tuple[CampaignStat]):
        response: Response = client.get("/?date_from=01-02-2002")
        assert response.status_code == 200
        assert response.json() == [
            {"date": "2002-02-02", "channel": "betcolony", "country": "US", "os": "ios", "impressions": 2000,
             "clicks": 200, "installs": 20, "spend": 22.2, "revenue": 222.2, "cpi": 1.11},
            {"date": "2003-03-03", "channel": "cedcolony", "country": "DE", "os": "windows", "impressions": 3000,
             "clicks": 300, "installs": 30, "spend": 33.3, "revenue": 333.3, "cpi": 1.11},
        ]

    def test_filters_date_to(self, client: TestClient, data_sample: tuple[CampaignStat]):
        response: Response = client.get("/?date_to=03-03-2002")
        assert response.status_code == 200
        assert response.json() == [
            {"date": "2001-01-01", "channel": "adcolony", "country": "RU", "os": "android", "impressions": 1000,
             "clicks": 100, "installs": 10, "spend": 11.1, "revenue": 111.1, "cpi": 1.11},
            {"date": "2002-02-02", "channel": "betcolony", "country": "US", "os": "ios", "impressions": 2000,
             "clicks": 200, "installs": 20, "spend": 22.2, "revenue": 222.2, "cpi": 1.11},
        ]

    def test_filters_channels(self, client: TestClient, data_sample: tuple[CampaignStat]):
        response: Response = client.get("/?channels=adcolony&channels=cedcolony")
        assert response.status_code == 200
        assert response.json() == [
            {"date": "2001-01-01", "channel": "adcolony", "country": "RU", "os": "android", "impressions": 1000,
             "clicks": 100, "installs": 10, "spend": 11.1, "revenue": 111.1, "cpi": 1.11},
            {"date": "2003-03-03", "channel": "cedcolony", "country": "DE", "os": "windows", "impressions": 3000,
             "clicks": 300, "installs": 30, "spend": 33.3, "revenue": 333.3, "cpi": 1.11},
        ]

    def test_filters_countries(self, client: TestClient, data_sample: tuple[CampaignStat]):
        response: Response = client.get("/?countries=US&countries=RU")
        assert response.status_code == 200
        assert response.json() == [
            {"date": "2001-01-01", "channel": "adcolony", "country": "RU", "os": "android", "impressions": 1000,
             "clicks": 100, "installs": 10, "spend": 11.1, "revenue": 111.1, "cpi": 1.11},
            {"date": "2002-02-02", "channel": "betcolony", "country": "US", "os": "ios", "impressions": 2000,
             "clicks": 200, "installs": 20, "spend": 22.2, "revenue": 222.2, "cpi": 1.11},
        ]

    def test_filters_oses(self, client: TestClient, data_sample: tuple[CampaignStat]):
        response: Response = client.get("/?os=android&os=windows&ordering=left")
        assert response.status_code == 200
        assert response.json() == [
            {"date": "2001-01-01", "channel": "adcolony", "country": "RU", "os": "android", "impressions": 1000,
             "clicks": 100, "installs": 10, "spend": 11.1, "revenue": 111.1, "cpi": 1.11},
            {"date": "2003-03-03", "channel": "cedcolony", "country": "DE", "os": "windows", "impressions": 3000,
             "clicks": 300, "installs": 30, "spend": 33.3, "revenue": 333.3, "cpi": 1.11},
        ]

    def test_sort_ascending(self, client: TestClient, data_sample: tuple[CampaignStat]):
        response: Response = client.get("/?sort=country")
        assert response.status_code == 200
        assert response.json() == [
            {"date": "2003-03-03", "channel": "cedcolony", "country": "DE", "os": "windows", "impressions": 3000,
             "clicks": 300, "installs": 30, "spend": 33.3, "revenue": 333.3, "cpi": 1.11},
            {"date": "2001-01-01", "channel": "adcolony", "country": "RU", "os": "android", "impressions": 1000,
             "clicks": 100, "installs": 10, "spend": 11.1, "revenue": 111.1, "cpi": 1.11},
            {"date": "2002-02-02", "channel": "betcolony", "country": "US", "os": "ios", "impressions": 2000,
             "clicks": 200, "installs": 20, "spend": 22.2, "revenue": 222.2, "cpi": 1.11},
        ]

    def test_sort_descending(self, client: TestClient, data_sample: tuple[CampaignStat]):
        response: Response = client.get("/?sort=country&ordering=desc")
        assert response.status_code == 200
        assert response.json() == [
            {"date": "2002-02-02", "channel": "betcolony", "country": "US", "os": "ios", "impressions": 2000,
             "clicks": 200, "installs": 20, "spend": 22.2, "revenue": 222.2, "cpi": 1.11},
            {"date": "2001-01-01", "channel": "adcolony", "country": "RU", "os": "android", "impressions": 1000,
             "clicks": 100, "installs": 10, "spend": 11.1, "revenue": 111.1, "cpi": 1.11},
            {"date": "2003-03-03", "channel": "cedcolony", "country": "DE", "os": "windows", "impressions": 3000,
             "clicks": 300, "installs": 30, "spend": 33.3, "revenue": 333.3, "cpi": 1.11},
        ]

    def test_group_by(self, client: TestClient, groupby_dataset):
        response: Response = client.get("/?groupby=country")
        assert response.status_code == 200
        result: list[dict] = response.json()
        result.sort(key=lambda obj: obj['country'])
        assert result == [
            {"date": None, "channel": None, "country": "DE", "os": None, "impressions": 9000, "clicks": 900,
             "installs": 90, "spend": 99.9, "revenue": 999.9, "cpi": 1.11},
            {"date": None, "channel": None, "country": "RU", "os": None, "impressions": 3000, "clicks": 300,
             "installs": 30, "spend": 33.3, "revenue": 333.3, "cpi": 1.11},
            {"date": None, "channel": None, "country": "US", "os": None, "impressions": 6000, "clicks": 600,
             "installs": 60, "spend": 66.6, "revenue": 666.6, "cpi": 1.11},
        ]

    def test_group_by_with_filtering(self, client: TestClient, groupby_dataset):
        response: Response = client.get("/?countries=DE&groupby=country")
        assert response.status_code == 200
        assert response.json() == [
            {"date": None, "channel": None, "country": "DE", "os": None, "impressions": 9000, "clicks": 900,
             "installs": 90, "spend": 99.9, "revenue": 999.9, "cpi": 1.11},
        ]

"""populate db

Revision ID: 18e0feb0c568
Revises: 3bdd0aa05420
Create Date: 2023-06-20 20:35:17.653225

"""
from pathlib import Path
from csv import DictReader
from typing import Generator
from alembic import op
from datetime import datetime as dt

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
this_path = Path(__file__).parent


class CampaignStat(Base):
    __tablename__ = 'campaign_stat'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    date = sa.Column(sa.Date, nullable=False)
    channel = sa.Column(sa.String, nullable=False)
    country = sa.Column(sa.String, nullable=False)
    os = sa.Column(sa.String, nullable=False)
    impressions = sa.Column(sa.Integer, nullable=False, default=0)
    clicks = sa.Column(sa.Integer, nullable=False, default=0)
    installs = sa.Column(sa.Integer, nullable=False, default=0)
    spend = sa.Column(sa.Numeric, nullable=False, default="0")
    revenue = sa.Column(sa.Numeric, nullable=False, default="0")


# revision identifiers, used by Alembic.
revision = '18e0feb0c568'
down_revision = '3bdd0aa05420'
branch_labels = None
depends_on = None


def read_stat_file(path: Path) -> Generator[dict, None, None]:
    row: dict
    with open(path) as file:
        csv_reader = DictReader(file)
        for row in csv_reader:
            date = row.get('date')
            # The better way is to use smth like a pydantic model, but it's sufficient for a test work.
            row['date'] = dt.strptime(date, '%Y-%m-%d')
            yield row


def upgrade() -> None:
    connection = op.get_bind()
    session = orm.Session(bind=connection)
    stats: list[CampaignStat] = []
    path = this_path / 'sample_dataset.csv'

    for row in read_stat_file(path):
        stat = CampaignStat(**row)
        stats.append(stat)

    session.add_all(stats)
    session.commit()


def downgrade() -> None:
    connection = op.get_bind()
    session = orm.Session(bind=connection)

    # You probably would not do that on production, but it's sufficient for a test work.
    session.execute(sa.delete(CampaignStat))
    session.commit()

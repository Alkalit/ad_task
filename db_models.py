from typing import NewType

from sqlalchemy import Column, Integer, Date, String, Numeric
from database import Base

__all__ = ['CampaignStat', 'ColumnName']


class CampaignStat(Base):
    __tablename__ = 'campaign_stat'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    channel = Column(String, nullable=False)
    country = Column(String, nullable=False)
    os = Column(String, nullable=False)
    impressions = Column(Integer, nullable=False, default=0)
    clicks = Column(Integer, nullable=False, default=0)
    installs = Column(Integer, nullable=False, default=0)
    spend = Column(Numeric, nullable=False, default="0")
    revenue = Column(Numeric, nullable=False, default="0")


ColumnName = NewType('ColumnName', str)

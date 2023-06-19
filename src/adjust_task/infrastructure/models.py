from sqlalchemy import Column, Integer, Date, String, Numeric
from sqlalchemy.ext.declarative import declarative_base

__all__ = ['CampaignStat', 'Base']

Base = declarative_base()


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

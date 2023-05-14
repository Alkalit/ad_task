from typing import NewType
from datetime import date as pydate
from decimal import Decimal
from pydantic import BaseModel

CampaignStatId = NewType('CampaignStatId', int)
Channel = NewType('Channel', str)
Country = NewType('Country', str)
OS = NewType('OS', str)
Money = NewType('Money', Decimal)


class CampaignStat(BaseModel):
    date: pydate
    channel: Channel
    country: Country
    os: OS
    impressions: int
    clicks: int
    installs: int
    spend: Money
    revenue: Money

    class Config:
        orm_mode = True

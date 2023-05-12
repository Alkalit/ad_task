from dataclasses import dataclass
from typing import NewType, Optional
from datetime import date as pydate
from decimal import Decimal

CampaignStatId = NewType('CampaignStatId', int)
Channel = NewType('Channel', str)
Country = NewType('Country', str)
Os = NewType('Os', str)
Money = NewType('Money', Decimal)


@dataclass()
class CampaignStat:
    id: Optional[CampaignStatId]
    date: pydate
    channel: Channel
    country: Country
    os: Os
    impressions: int
    clicks: int
    installs: int
    spend: Money
    revenue: Money

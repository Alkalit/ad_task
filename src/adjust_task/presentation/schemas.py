from typing import NewType
from datetime import date
from pydantic import BaseModel

from adjust_task.domain.models import Money

CampaignStatId = NewType('CampaignStatId', int)
Channel = NewType('Channel', str)
Country = NewType('Country', str)
OS = NewType('OS', str)


class CampaignStatSchema(BaseModel):
    date: date | None
    channel: Channel | None
    country: Country | None
    os: OS | None
    impressions: int
    clicks: int
    installs: int
    spend: Money
    revenue: Money
    cpi: Money

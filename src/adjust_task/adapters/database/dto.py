from dataclasses import dataclass
from datetime import date

from pydantic import BaseModel

from adjust_task.domain.models import Money, ColumnName


class CampaignStatsDTO(BaseModel):

    date: date | None
    channel: ColumnName | None
    country: ColumnName | None
    os: ColumnName | None
    impressions: int
    clicks: int
    installs: int
    spend: Money
    revenue: Money
    cpi: Money

    class Config:
        orm_mode = True


@dataclass
class StatisticsDTO:
    date_from: date | None
    date_to: date | None
    channels: list[ColumnName] | None
    countries: list[ColumnName] | None
    os: list[ColumnName] | None

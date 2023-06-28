from dataclasses import dataclass, fields
from datetime import date
from typing import Generator, Any

from pydantic import BaseModel

from adjust_task.application.models import ColumnName
from adjust_task.presentation.schemas import Money

__all__ = ['CampaignStatsDTO', 'StatisticsDTO']


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

    def __iter__(self):
        for field in fields(self):
            value = getattr(self, field.name)
            yield field.name, value

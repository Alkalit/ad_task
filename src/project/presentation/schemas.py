from typing import NewType
from datetime import date

from _decimal import Decimal
from fastapi import Query
from pydantic import BaseModel, Field

from project.application.models import SortableFields, GroupbyFields, Ordering

__all__ = ['CampaignStatParams', 'CampaignStatSchema']


Channel = NewType('Channel', str)
Country = NewType('Country', str)
OS = NewType('OS', str)
Money = NewType('Money', Decimal)


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


class CampaignStatParams(BaseModel):
    date_from: date | None = Field(Query(None))
    date_to: date | None = Field(Query(None))
    channels: list[str] | None = Field(Query(None))
    countries: list[str] | None = Field(Query(None))
    os: list[str] | None = Field(Query(None))
    sort: SortableFields | None = Field(Query(None))
    groupby: list[GroupbyFields] | None = Field(Query(None))
    ordering: Ordering = Field(Query(Ordering.asc))

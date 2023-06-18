from typing import NewType
from datetime import date

from fastapi import Query
from pydantic import BaseModel, Field

from adjust_task.domain.models import Money, StatSortableFields, GroupbyFields, StatOrdering

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


class CampaignStatParams(BaseModel):
    date_from: date | None = Field(Query(None))
    date_to: date | None = Field(Query(None))
    channels: list[str] | None = Field(Query(None))
    countries: list[str] | None = Field(Query(None))
    os: list[str] | None = Field(Query(None))
    sort: StatSortableFields | None = Field(Query(None))
    groupby: list[GroupbyFields] | None = Field(Query(None))
    ordering: StatOrdering = Field(Query(StatOrdering.asc))

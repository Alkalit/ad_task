from enum import Enum

from fastapi import Query
from pydantic import BaseModel, Field


class GroupbyFields(str, Enum):
    date = 'date'
    channel = 'channel'
    country = 'country'
    os = 'os'


class StatOrdering(str, Enum):
    asc = 'asc'
    desc = 'desc'


class StatSortableFields(str, Enum):
    date = 'date'
    channel = 'channel'
    country = 'country'
    os = 'os'
    impressions = 'impressions'
    clicks = 'clicks'
    installs = 'installs'
    spend = 'spend'
    revernue = 'revenue'


class StatParams(BaseModel):
    date_from: str | None = Field(Query(None))
    date_to: str | None = Field(Query(None))
    channels: list[str] | None = Field(Query(None))
    countries: list[str] | None = Field(Query(None))
    os: list[str] | None = Field(Query(None))
    sort: StatSortableFields | None = Field(Query(None))
    groupby: list[GroupbyFields] | None = Field(Query(None))
    ordering: StatOrdering = Field(Query(StatOrdering.asc))

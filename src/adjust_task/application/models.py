from enum import Enum


# pydantic doesn't want to work with NewType
class ColumnName(str):
    pass


class GroupbyFields(ColumnName, Enum):
    date = 'date'
    channel = 'channel'
    country = 'country'
    os = 'os'


class StatOrdering(ColumnName, Enum):
    asc = 'asc'
    desc = 'desc'


class StatSortableFields(ColumnName, Enum):
    date = 'date'
    channel = 'channel'
    country = 'country'
    os = 'os'
    impressions = 'impressions'
    clicks = 'clicks'
    installs = 'installs'
    spend = 'spend'
    revenue = 'revenue'

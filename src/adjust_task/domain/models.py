from enum import Enum
from typing import NewType

from decimal import Decimal


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
    revenue = 'revenue'


Money = NewType('Money', Decimal)

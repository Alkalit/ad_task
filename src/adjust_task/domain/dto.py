from dataclasses import dataclass
from datetime import date
from adjust_task.infrastructure.models import ColumnName


@dataclass
class StatisticsDTO:
    date_from: date | None
    date_to: date | None
    channels: list[ColumnName] | None
    countries: list[ColumnName] | None
    os: list[ColumnName] | None

from dataclasses import dataclass
from datetime import date


class BaseSpecification:
    ...


@dataclass
class StatisticSpecification(BaseSpecification):
    date_from: date | None
    date_to: date | None
    channels: list[str] | None
    countries: list[str] | None
    os: list[str] | None
    groupby: list[str] | None

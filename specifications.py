from dataclasses import dataclass
from collections.abc import Callable
from datetime import date
from sqlalchemy import select, Select, null, func, Column

from db_models import CampaignStat
from models import GroupbyFields


class BaseSpecification(Callable):
    def __call__(self) -> Select:
        ...


@dataclass
class StatisticSpecification(BaseSpecification):
    date_from: date | None
    date_to: date | None
    channels: list[str] | None
    countries: list[str] | None
    os: list[str] | None

    def __call__(self) -> Select:
        expression = select(
            CampaignStat.date,
            CampaignStat.channel,
            CampaignStat.country,
            CampaignStat.os,
            CampaignStat.impressions,
            CampaignStat.clicks,
            CampaignStat.installs,
            CampaignStat.spend,
            CampaignStat.revenue,
            (CampaignStat.spend / CampaignStat.installs).label('cpi'),
        )

        if self.date_from:
            expression = expression.where(CampaignStat.date >= self.date_from)
        if self.date_to:
            expression = expression.where(CampaignStat.date < self.date_to)
        if self.channels:
            expression = expression.where(CampaignStat.channel.in_(self.channels))
        if self.countries:
            expression = expression.where(CampaignStat.country.in_(self.countries))
        if self.os:
            expression = expression.where(CampaignStat.os.in_(self.os))
        return expression


FIELDS_MAPPING: dict[str, Column] = {
    'date': CampaignStat.date,
    'channel': CampaignStat.channel,
    'country': CampaignStat.country,
    'os': CampaignStat.os,
}


@dataclass
class GroupBySpecification(BaseSpecification):
    date_from: date | None
    date_to: date | None
    channels: list[str] | None
    countries: list[str] | None
    os: list[str] | None
    groupby: list[str]

    def __call__(self) -> Select:
        columns_with_nulls: list[Column] = []
        columns: list[Column] = []
        fields: dict[GroupbyFields, int] = dict(zip(self.groupby, range(len(self.groupby))))

        for field in FIELDS_MAPPING:
            if field in fields:
                column = FIELDS_MAPPING[field]
                columns.append(column)
            else:
                column = null().label(field)
            columns_with_nulls.append(column)

        expression = select(
            # null().label("date"),
            # null().label("channel"),
            # null().label("country"),
            # null().label("os"),
            *columns_with_nulls,

            func.sum(CampaignStat.impressions).label(CampaignStat.impressions.name),
            func.sum(CampaignStat.clicks).label(CampaignStat.clicks.name),
            func.sum(CampaignStat.installs).label(CampaignStat.installs.name),
            func.sum(CampaignStat.spend).label(CampaignStat.spend.name),
            func.sum(CampaignStat.revenue).label(CampaignStat.revenue.name),
            (CampaignStat.spend / CampaignStat.installs).label('cpi'),
        ).group_by(*columns)

        if self.date_from:
            expression = expression.where(CampaignStat.date >= self.date_from)
        if self.date_to:
            expression = expression.where(CampaignStat.date < self.date_to)
        if self.channels:
            expression = expression.where(CampaignStat.channel.in_(self.channels))
        if self.countries:
            expression = expression.where(CampaignStat.country.in_(self.countries))
        if self.os:
            expression = expression.where(CampaignStat.os.in_(self.os))
        return expression

from datetime import date
from typing import Sequence

from sqlalchemy import select, Select, null, func, Column, asc, desc, Column, Row
from sqlalchemy.orm import Session
from specifications import StatisticSpecification

from db_models import CampaignStat
from models import GroupbyFields
from models import StatOrdering, GroupbyFields


class BaseRepository:
    ...


class CampaignStatisticsRepository(BaseRepository):

    FIELDS_MAPPING: dict[str, Column] = {
        'date': CampaignStat.date,
        'channel': CampaignStat.channel,
        'country': CampaignStat.country,
        'os': CampaignStat.os,
    }

    def __init__(self, session: Session):
        self._session = session

    def select_campaign_stats(self,
                              spec: StatisticSpecification,
                              sort: str | None = None,
                              ordering: str | None = None,
                              ) -> Sequence[Row]:

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

        if spec.date_from:
            expression = expression.where(CampaignStat.date >= spec.date_from)
        if spec.date_to:
            expression = expression.where(CampaignStat.date < spec.date_to)
        if spec.channels:
            expression = expression.where(CampaignStat.channel.in_(spec.channels))
        if spec.countries:
            expression = expression.where(CampaignStat.country.in_(spec.countries))
        if spec.os:
            expression = expression.where(CampaignStat.os.in_(spec.os))

        if sort:
            field = self.FIELDS_MAPPING.get(sort)
            if ordering == StatOrdering.asc:
                direction = asc
            else:
                direction = desc
            expression = expression.order_by(direction(field))

        stats = self._session.execute(expression).all()
        return stats

    def select_campaign_analytical_stats(self,
                                         spec: StatisticSpecification,
                                         sort: str | None = None,
                                         ordering: str | None = None,
                                         ) -> Sequence[Row]:

        columns_with_nulls: list[Column] = []
        columns: list[Column] = []
        fields: dict[GroupbyFields, int] = dict(zip(spec.groupby, range(len(spec.groupby))))

        for field in self.FIELDS_MAPPING:
            if field in fields:
                column = self.FIELDS_MAPPING[field]
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

        if spec.date_from:
            expression = expression.where(CampaignStat.date >= spec.date_from)
        if spec.date_to:
            expression = expression.where(CampaignStat.date < spec.date_to)
        if spec.channels:
            expression = expression.where(CampaignStat.channel.in_(spec.channels))
        if spec.countries:
            expression = expression.where(CampaignStat.country.in_(spec.countries))
        if spec.os:
            expression = expression.where(CampaignStat.os.in_(spec.os))

        if sort:
            field = self.FIELDS_MAPPING.get(sort)
            if ordering == StatOrdering.asc:
                direction = asc
            else:
                direction = desc
            expression = expression.order_by(direction(field))

        stats = self._session.execute(expression).all()
        return stats

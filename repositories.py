from typing import Sequence, Protocol

from sqlalchemy import select, Select, null, func, asc, desc, Column, Row, ColumnElement
from sqlalchemy.orm import Session
from specifications import StatisticSpecification

from db_models import CampaignStat
from models import StatOrdering, GroupbyFields


class ICampaignStatisticsRepository(Protocol):

    def select_campaign_analytical_stats(self,
                                         spec: StatisticSpecification,
                                         sort: str | None = None,
                                         ordering: str | None = None,
                                         ) -> Sequence[Row]:
        ...

    def select_campaign_stats(self,
                              spec: StatisticSpecification,
                              sort: str | None = None,
                              ordering: str | None = None,
                              ) -> Sequence[Row]:
        ...


# TODO rename to gateway
class CampaignStatisticsRepository:

    FIELDS_MAPPING: dict[str, Column] = {
        'date': CampaignStat.date,
        'channel': CampaignStat.channel,
        'country': CampaignStat.country,
        'os': CampaignStat.os,
    }

    def __init__(self, session: Session):
        self._session = session

    def _setup_select_clause(self, *columns: ColumnElement) -> Select:

        expression = select(*columns)

        return expression

    def _setup_sql_params(self,
                          expression: Select,
                          spec: StatisticSpecification,
                          sort: str | None = None,
                          ordering: str | None = None,
                          groupby: list[ColumnElement] = None,
                          ) -> Select:

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

        if groupby:
            expression = expression.group_by(*groupby)

        return expression

    def _execute(self, expression: Select) -> Sequence[Row]:
        result = self._session.execute(expression).all()
        return result

    def select_campaign_stats(self,
                              spec: StatisticSpecification,
                              sort: str | None = None,
                              ordering: str | None = None,
                              ) -> Sequence[Row]:

        expression = self._setup_select_clause(
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

        expression = self._setup_sql_params(expression, spec, sort, ordering)

        stats = self._execute(expression)
        return stats

    def select_campaign_analytical_stats(self,
                                         spec: StatisticSpecification,
                                         sort: str | None = None,
                                         ordering: str | None = None,
                                         ) -> Sequence[Row]:

        columns_with_nulls: list[Column] = []
        groupby_columns: list[Column] = []
        fields: dict[GroupbyFields, int] = dict(zip(spec.groupby, range(len(spec.groupby))))

        for field in self.FIELDS_MAPPING:
            if field in fields:
                column = self.FIELDS_MAPPING[field]
                groupby_columns.append(column)
            else:
                column = null().label(field)
            columns_with_nulls.append(column)

        expression = self._setup_select_clause(
            *columns_with_nulls,
            func.sum(CampaignStat.impressions).label(CampaignStat.impressions.name),
            func.sum(CampaignStat.clicks).label(CampaignStat.clicks.name),
            func.sum(CampaignStat.installs).label(CampaignStat.installs.name),
            func.sum(CampaignStat.spend).label(CampaignStat.spend.name),
            func.sum(CampaignStat.revenue).label(CampaignStat.revenue.name),
            (CampaignStat.spend / CampaignStat.installs).label('cpi'),
        )

        expression = self._setup_sql_params(expression, spec, sort, ordering, groupby_columns)

        stats = self._execute(expression)
        return stats

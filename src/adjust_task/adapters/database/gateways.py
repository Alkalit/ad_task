from typing import Protocol, NewType

from pydantic import parse_obj_as

from sqlalchemy import select, Select, null, func, asc, desc, Column, ColumnElement, inspect
from sqlalchemy.orm import Session, Mapper

from adjust_task.adapters.database.dto import CampaignStatsDTO, StatisticsDTO
from adjust_task.infrastructure.models import CampaignStat
from adjust_task.application.models import StatOrdering, GroupbyFields as GbF, StatSortableFields as SSF


NullColumn = NewType('NullColumn', ColumnElement)


class ICampaignStatisticsGateway(Protocol):

    def select_campaign_analytical_stats(self,
                                         spec: StatisticsDTO,
                                         groupbys: list[GbF],
                                         align_columns: list[GbF],
                                         sort: SSF | None = None,
                                         ordering: StatOrdering | None = None,
                                         ) -> list[CampaignStatsDTO]:
        ...

    def select_campaign_stats(self,
                              spec: StatisticsDTO,
                              sort: SSF | None = None,
                              ordering: StatOrdering | None = None,
                              ) -> list[CampaignStatsDTO]:
        ...


class CampaignStatisticsGateway:

    def __init__(self, session: Session):
        self._session = session
        self.mapper: Mapper = inspect(CampaignStat)

    def _setup_select_clause(self, *columns: ColumnElement) -> Select:
        expression = select(*columns)

        return expression

    def _setup_sql_params(self,
                          expression: Select,
                          spec: StatisticsDTO,
                          sort: SSF | None = None,
                          ordering: StatOrdering | None = None,
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
            field = self.mapper.columns[sort]
            if ordering == StatOrdering.asc:
                direction = asc
            else:
                direction = desc
            expression = expression.order_by(direction(field))

        if groupby:
            expression = expression.group_by(*groupby)

        return expression

    def _execute(self, expression: Select) -> list[CampaignStatsDTO]:
        raws = self._session.execute(expression).all()
        stats = parse_obj_as(list[CampaignStatsDTO], raws)
        return stats

    def _get_groupbys(self,
                      groupbys: list[GbF],
                      align_columns: list[GbF]
                      ) -> tuple[list[NullColumn], list[Column]]:

        nulled_column: list[NullColumn] = []
        groupby_columns: list[Column] = []
        fields: dict[GbF, int] = dict(zip(groupbys, range(len(groupbys))))

        for field in align_columns:
            if field in fields:
                column = self.mapper.columns[field]
                groupby_columns.append(column)
            else:
                column = null().label(field)
            nulled_column.append(column)

        return nulled_column, groupby_columns

    def select_campaign_stats(self,
                              spec: StatisticsDTO,
                              sort: SSF | None = None,
                              ordering: StatOrdering | None = None,
                              ) -> list[CampaignStatsDTO]:

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
                                         spec: StatisticsDTO,
                                         groupbys: list[GbF],
                                         align_columns: list[GbF],
                                         sort: SSF | None = None,
                                         ordering: StatOrdering | None = None,
                                         ) -> list[CampaignStatsDTO]:

        columns_with_nulls, groupby_columns = self._get_groupbys(groupbys, align_columns)

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

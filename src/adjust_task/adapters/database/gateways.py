from pydantic import parse_obj_as

from sqlalchemy import select, Select, asc, desc, Column, ColumnElement, inspect
from sqlalchemy.orm import Session, Mapper

from adjust_task.adapters.database.dto import CampaignStatsDTO, StatisticsDTO
from adjust_task.infrastructure.models import CampaignStat
from adjust_task.application.models import Ordering, GroupbyFields as GbF, SortableFields as SrtF, ColumnName


__all__ = ['CampaignStatisticsGateway']


class CampaignStatisticsGateway:

    def __init__(self, session: Session):
        self._session = session
        self._mapper: Mapper = inspect(CampaignStat)

    def _setup_select_clause(self, *columns: ColumnElement) -> Select:
        expression = select(*columns)

        return expression

    def _setup_sql_params(self,
                          expression: Select,
                          spec: StatisticsDTO,
                          sort: SrtF | None = None,
                          ordering: Ordering = Ordering.asc,
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
            [field] = self._get_columns_by_name([sort])
            if ordering == Ordering.asc:
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

    def _get_columns_by_name(self,
                             column_names: list[ColumnName],
                             ) -> list[Column]:

        columns: list[Column] = []

        for name in column_names:
            column = self._mapper.columns[name]
            columns.append(column)

        return columns

    def select_campaign_analytical_stats(self,
                                         to_select: list[ColumnElement],
                                         spec: StatisticsDTO,
                                         groupbys: list[GbF] = None,
                                         sort: SrtF | None = None,
                                         ordering: Ordering = Ordering.asc,
                                         ) -> list[CampaignStatsDTO]:

        if groupbys:
            groupby_columns = self._get_columns_by_name(groupbys)
            expression = self._setup_select_clause(
                *groupby_columns,
                *to_select,
            )
        else:
            groupby_columns = None
            expression = self._setup_select_clause(
                *to_select,
            )

        expression = self._setup_sql_params(expression, spec, sort, ordering, groupby_columns)

        stats = self._execute(expression)
        return stats

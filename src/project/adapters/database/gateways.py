import operator as op
from typing import Any, Callable

from pydantic import parse_obj_as

from sqlalchemy import select, Select, asc, desc, Column, ColumnElement, inspect
from sqlalchemy.orm import Mapper
from sqlalchemy.ext.asyncio import AsyncSession

from project.adapters.database.dto import CampaignStatsDTO, StatisticsDTO
from project.infrastructure.models import CampaignStat
from project.application.models import Ordering, GroupbyFields as GbF, SortableFields as SrtF, ColumnName

__all__ = ['CampaignStatisticsGateway']


class GatewayException(Exception):
    pass


class CampaignStatisticsGateway:
    FILTER_COLUMNS: dict[str, Callable[[Any], Any]] = {
        'date_from': lambda arg: op.ge(CampaignStat.date, arg),
        'date_to': lambda arg: op.lt(CampaignStat.date, arg),
        'channels': lambda arg: CampaignStat.channel.in_(arg),
        'countries': lambda arg: CampaignStat.country.in_(arg),
        'os': lambda arg: CampaignStat.os.in_(arg),
    }

    def __init__(self, session: AsyncSession):
        self._session = session
        self._mapper: Mapper = inspect(CampaignStat)

    def _setup_select_clause(self, *columns: ColumnElement) -> Select:
        expression = select(*columns)

        return expression

    def _setup_sql_params(self,
                          expression: Select,
                          filters: StatisticsDTO,
                          sort: SrtF | None = None,
                          ordering: Ordering = Ordering.asc,
                          groupby: list[ColumnElement] = None,
                          ) -> Select:

        for field_name, value in filters:
            if value is None:
                continue
            try:
                filter_ = self.FILTER_COLUMNS[field_name]
            except KeyError as ex:
                raise GatewayException(f"Unknown field: {field_name}") from ex

            expression = expression.where(filter_(value))

        if sort:
            if ordering == Ordering.asc:
                direction = asc
            else:
                direction = desc
            expression = expression.order_by(direction(sort))

        if groupby:
            expression = expression.group_by(*groupby)

        return expression

    async def _execute(self, expression: Select) -> list[CampaignStatsDTO]:
        rows = (await self._session.execute(expression)).all()
        stats = parse_obj_as(list[CampaignStatsDTO], rows)
        return stats

    def _get_columns_by_name(self,
                             column_names: list[ColumnName],
                             ) -> list[Column]:

        columns: list[Column] = []

        for name in column_names:
            column = self._mapper.columns[name]
            columns.append(column)

        return columns

    async def select_campaign_analytical_stats(self,
                                               to_select: list[ColumnElement],
                                               filters: StatisticsDTO,
                                               sort: SrtF | None = None,
                                               ordering: Ordering = Ordering.asc,
                                               groupbys: list[GbF] = None,
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

        expression = self._setup_sql_params(expression, filters, sort, ordering, groupby_columns)

        stats = await self._execute(expression)
        return stats

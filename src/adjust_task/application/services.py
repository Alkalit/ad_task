from collections.abc import Callable

from pydantic import BaseModel

from adjust_task.infrastructure.db_models import ColumnName
from adjust_task.domain.models import StatParams
from adjust_task.domain.specifications import StatisticSpecification
from adjust_task.adapters.database.gateways import ICampaignStatisticsGateway, CampaignStatsDTO


class Service(Callable):

    def __init__(self, campaign_gateway: ICampaignStatisticsGateway):
        self.campaign_gateway = campaign_gateway

    def __call__(self, params: BaseModel):
        ...


class AnalyticsService(Service):

    def __call__(self, params: StatParams) -> list[CampaignStatsDTO]:
        spec = StatisticSpecification(
            date_from=params.date_from,
            date_to=params.date_to,
            channels=params.channels,
            countries=params.countries,
            os=params.os,
        )

        if params.groupby:
            align_columns: list[ColumnName] = ['date', 'channel', 'country', 'os']
            stats = self.campaign_gateway.select_campaign_analytical_stats(
                spec,
                params.groupby,
                align_columns,
                params.sort,
                params.ordering,
            )
        else:
            stats = self.campaign_gateway.select_campaign_stats(spec, params.sort, params.ordering)

        return stats

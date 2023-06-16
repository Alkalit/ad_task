from collections.abc import Callable

from pydantic import BaseModel

from db_models import ColumnName
from models import StatParams
from specifications import StatisticSpecification
from gateways import ICampaignStatisticsGateway, CampaignStatsDTO


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

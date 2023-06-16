from collections.abc import Callable
from typing import Sequence

from sqlalchemy import Row
from pydantic import BaseModel

from models import StatParams
from specifications import StatisticSpecification
from gateways import ICampaignStatisticsGateway


class Service(Callable):

    def __init__(self, campaign_gateway: ICampaignStatisticsGateway):
        self.campaign_gateway = campaign_gateway

    def __call__(self, params: BaseModel):
        ...


class AnalyticsService(Service):

    # TODO return models
    def __call__(self, params: StatParams) -> Sequence[Row]:
        spec = StatisticSpecification(
            date_from=params.date_from,
            date_to=params.date_to,
            channels=params.channels,
            countries=params.countries,
            os=params.os,
            groupby=params.groupby,
        )

        if params.groupby:
            stats = self.campaign_gateway.select_campaign_analytical_stats(spec, params.sort, params.ordering)
        else:
            stats = self.campaign_gateway.select_campaign_stats(spec, params.sort, params.ordering)

        return stats

from collections.abc import Callable

from pydantic import BaseModel
from sqlalchemy import func

from adjust_task.presentation.schemas import CampaignStatParams
from adjust_task.adapters.database.gateways import CampaignStatisticsGateway
from adjust_task.adapters.database.dto import CampaignStatsDTO, StatisticsDTO
from adjust_task.infrastructure.models import CampaignStat

__all__ = ['Service', 'AnalyticsService']


class Service(Callable):

    def __init__(self, campaign_gateway: CampaignStatisticsGateway):
        self.campaign_gateway = campaign_gateway

    def __call__(self, params: BaseModel):
        ...


class AnalyticsService(Service):

    def __call__(self, params: CampaignStatParams) -> list[CampaignStatsDTO]:
        filters = StatisticsDTO(
            date_from=params.date_from,
            date_to=params.date_to,
            channels=params.channels,
            countries=params.countries,
            os=params.os,
        )

        if params.groupby:
            to_select = \
                [
                    func.sum(CampaignStat.impressions).label(CampaignStat.impressions.name),
                    func.sum(CampaignStat.clicks).label(CampaignStat.clicks.name),
                    func.sum(CampaignStat.installs).label(CampaignStat.installs.name),
                    func.sum(CampaignStat.spend).label(CampaignStat.spend.name),
                    func.sum(CampaignStat.revenue).label(CampaignStat.revenue.name),
                    (CampaignStat.spend / CampaignStat.installs).label('cpi'),
                ]
        else:
            to_select = \
                [
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
                ]

        stats = self.campaign_gateway.select_campaign_analytical_stats(
            to_select,
            filters,
            params.sort,
            params.ordering,
            params.groupby,
        )

        return stats

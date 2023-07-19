from sqlalchemy import func

from project.presentation.schemas import CampaignStatParams
from project.adapters.database.gateways import CampaignStatisticsGateway
from project.adapters.database.dto import CampaignStatsDTO, StatisticsDTO
from project.infrastructure.models import CampaignStat

__all__ = ['AnalyticsService']


class AnalyticsService:

    def __init__(self, campaign_gateway: CampaignStatisticsGateway):
        self.campaign_gateway = campaign_gateway

    async def __call__(self, params: CampaignStatParams) -> list[CampaignStatsDTO]:
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
                    (func.sum(CampaignStat.spend) / func.sum(CampaignStat.installs)).label('cpi'),
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

        stats = await self.campaign_gateway.select_campaign_analytical_stats(
            to_select,
            filters,
            params.sort,
            params.ordering,
            params.groupby,
        )

        return stats

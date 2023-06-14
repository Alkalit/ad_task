from collections.abc import Callable
from typing import Sequence

from sqlalchemy import asc, desc, Column, Row
from sqlalchemy.orm import Session
from pydantic import BaseModel

from db_models import CampaignStat
from models import StatOrdering, StatParams
from specifications import StatisticSpecification
from repositories import CampaignStatisticsRepository


class Service(Callable):

    def __init__(self, session: Session):
        self._session = session

    def __call__(self, params: BaseModel):
        ...


class AnalyticsService(Service):
    FIELDS_MAPPING: dict[str, Column] = {
        'date': CampaignStat.date,
        'channel': CampaignStat.channel,
        'country': CampaignStat.country,
        'os': CampaignStat.os,
    }

    # TODO hybrid properties
    def __call__(self, params: StatParams) -> Sequence[Row]:
        spec = StatisticSpecification(
            date_from=params.date_from,
            date_to=params.date_to,
            channels=params.channels,
            countries=params.countries,
            os=params.os,
            groupby=params.groupby,
        )

        # TODO DI into the service
        repo = CampaignStatisticsRepository(self._session)

        if params.groupby:
            stats = repo.select_campaign_analytical_stats(spec, params.sort, params.ordering)
        else:
            stats = repo.select_campaign_stats(spec, params.sort, params.ordering)

        return stats

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

    def __call__(self, params: StatParams) -> Sequence[Row]:
        spec = StatisticSpecification(
            date_from=params.date_from,
            date_to=params.date_to,
            channels=params.channels,
            countries=params.countries,
            os=params.os,
            groupby=params.groupby,
        )

        repo = CampaignStatisticsRepository(self._session)

        if params.groupby:
            expression = repo.select_campaign_analytical_stats(spec)
        else:
            expression = repo.select_campaign_stats(spec)

        # expression = specification()

        if params.sort:
            field = self.FIELDS_MAPPING.get(params.sort)
            if params.ordering == StatOrdering.asc:
                direction = asc
            else:
                direction = desc
            expression = expression.order_by(direction(field))
        stats = self._session.execute(expression).all()
        return stats

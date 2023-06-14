from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models import StatParams
from schemas import CampaignStatSchema
from services import AnalyticsService
from repositories import ICampaignStatisticsRepository, CampaignStatisticsRepository
from stub import Stub

router = APIRouter()


def get_campaign_repository(session: Annotated[Session, Depends(Stub(Session))]) -> ICampaignStatisticsRepository:
    return CampaignStatisticsRepository(session)


def get_service(
        campaign_repository: Annotated[ICampaignStatisticsRepository, Depends(get_campaign_repository)]
) -> AnalyticsService:
    return AnalyticsService(campaign_repository)


@router.get("/")
def root(
        params: Annotated[StatParams, Depends()],
        service: Annotated[AnalyticsService, Depends(get_service)],
) -> list[CampaignStatSchema]:
    stats = service(params)
    return stats

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from adjust_task.presentation.schemas import CampaignStatSchema, CampaignStatParams
from adjust_task.application.services import AnalyticsService
from adjust_task.adapters.database.gateways import CampaignStatisticsGateway
from adjust_task.presentation.utils import Stub

__all__ = ['router']

router = APIRouter()


def get_campaign_gateway(session: Annotated[Session, Depends(Stub(Session))]) -> CampaignStatisticsGateway:
    return CampaignStatisticsGateway(session)


def get_service(
        campaign_gateway: Annotated[CampaignStatisticsGateway, Depends(get_campaign_gateway)]
) -> AnalyticsService:
    return AnalyticsService(campaign_gateway)


@router.get("/")
def root(
        params: Annotated[CampaignStatParams, Depends()],
        service: Annotated[AnalyticsService, Depends(get_service)],
) -> list[CampaignStatSchema]:
    stats = service(params)
    return stats

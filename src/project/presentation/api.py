from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from project.presentation.schemas import CampaignStatSchema, CampaignStatParams
from project.application.services import AnalyticsService
from project.adapters.database.gateways import CampaignStatisticsGateway
from project.presentation.utils import Stub

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

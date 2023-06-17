from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models import StatParams
from schemas import CampaignStatSchema
from services import AnalyticsService
from gateways import ICampaignStatisticsGateway, CampaignStatisticsGateway
from stub import Stub

router = APIRouter()


def get_campaign_gateway(session: Annotated[Session, Depends(Stub(Session))]) -> CampaignStatisticsGateway:
    return CampaignStatisticsGateway(session)


def get_service(
        campaign_gateway: Annotated[ICampaignStatisticsGateway, Depends(get_campaign_gateway)]
) -> AnalyticsService:
    return AnalyticsService(campaign_gateway)


@router.get("/")
def root(
        params: Annotated[StatParams, Depends()],
        service: Annotated[AnalyticsService, Depends(get_service)],
) -> list[CampaignStatSchema]:
    stats = service(params)
    return stats

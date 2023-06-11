from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models import StatParams
from schemas import CampaignStatSchema
from services import AnalyticsService
from stub import Stub

router = APIRouter()


def get_service(session: Annotated[Session, Depends(Stub(Session))]) -> AnalyticsService:
    return AnalyticsService(session)


@router.get("/")
def root(
        params: Annotated[StatParams, Depends()],
        service: Annotated[AnalyticsService, Depends(get_service)],
) -> list[CampaignStatSchema]:
    stats = service(params)
    return stats

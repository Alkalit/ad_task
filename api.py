from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models import StatParams
from schemas import CampaignStatSchema
from services import BaseAnalyticsService
from stub import Stub

router = APIRouter()


@router.get("/")
def root(
        session: Annotated[Session, Depends(Stub(Session))],
        params: Annotated[StatParams, Depends()],
        service: Annotated[BaseAnalyticsService, Depends()],
) -> list[CampaignStatSchema]:
    stats = service(session, params)
    return stats

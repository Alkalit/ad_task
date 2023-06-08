from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models import StatParams
from schemas import CampaignStatSchema
from services import AnalyticsService
from stub import Stub

router = APIRouter()


@router.get("/")
def root(
        session: Annotated[Session, Depends(Stub(Session))],
        params: Annotated[StatParams, Depends()],
        service: Annotated[AnalyticsService, Depends()],
) -> list[CampaignStatSchema]:
    stats = service(session, params)
    return stats

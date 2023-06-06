from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models import StatParams
from schemas import CampaignStatSchema
from services import analytics_service
from stub import Stub

router = APIRouter()


@router.get("/")
def root(
        session: Annotated[Session, Depends(Stub(Session))],
        params: StatParams = Depends(),
) -> list[CampaignStatSchema]:
    stats = analytics_service(params, session)
    return stats

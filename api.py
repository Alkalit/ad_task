from typing import Annotated
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from db_models import CampaignStat
from schemas import CampaignStatSchema
from stub import Stub

router = APIRouter()


@router.get("/")
def root(session: Annotated[Session, Depends(Stub(Session))]) -> list[CampaignStatSchema]:
    stats = session.query(CampaignStat).all()
    return stats

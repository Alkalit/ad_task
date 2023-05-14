from fastapi import APIRouter
from database import SessionFactory
from db_models import CampaignStat
from models import CampaignStat as CampaignStatSchema

router = APIRouter()


@router.get("/")
def root() -> list[CampaignStatSchema]:
    session = SessionFactory()
    stats = session.query(CampaignStat).all()
    return stats

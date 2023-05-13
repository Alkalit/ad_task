from fastapi import APIRouter
from database import SessionFactory, Base, engine
from db_models import CampaignStat
from models import CampaignStat as CampaignStatSchema

router = APIRouter()
Base.metadata.create_all(bind=engine)


@router.get("/")
def root() -> list[CampaignStatSchema]:
    session = SessionFactory()
    stats = session.query(CampaignStat).all()
    return stats

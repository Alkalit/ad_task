from typing import Annotated
from datetime import datetime, date

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from db_models import CampaignStat
from schemas import CampaignStatSchema
from stub import Stub

router = APIRouter()


@router.get("/")
def root(
    session: Annotated[Session, Depends(Stub(Session))],
    date_from: Annotated[str | None, Query()] = None,
    date_to: Annotated[str | None, Query()] = None,
    channels: Annotated[list[str] | None, Query()] = None,
    countries: Annotated[list[str] | None, Query()] = None,
    os: Annotated[list[str] | None, Query()] = None,
) -> list[CampaignStatSchema]:

    expression = select(CampaignStat)

    if date_from:
        date_from: date = datetime.strptime(date_from, '%d-%m-%Y').date()
        expression = expression.where(CampaignStat.date >= date_from)
    if date_to:
        date_to: date = datetime.strptime(date_to, '%d-%m-%Y').date()
        expression = expression.where(CampaignStat.date <= date_to)
    if channels:
        expression = expression.where(CampaignStat.channel.in_(channels))
    if countries:
        expression = expression.where(CampaignStat.country.in_(countries))
    if os:
        expression = expression.where(CampaignStat.os.in_(os))

    stats = session.scalars(expression).all()
    return stats

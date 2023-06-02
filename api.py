from typing import Annotated
from datetime import datetime, date

from fastapi import APIRouter, Depends
from sqlalchemy import select, Column, desc, asc, func
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import null

from db_models import CampaignStat
from models import StatParams, StatOrdering
from schemas import CampaignStatSchema
from stub import Stub

router = APIRouter()

# TODO validation error
SORT_FIELDS_MAPPING: dict[str, Column] = {
    'date': CampaignStat.date,
    'channel': CampaignStat.channel,
    'country': CampaignStat.country,
    'os': CampaignStat.os,
}


@router.get("/")
def root(
        session: Annotated[Session, Depends(Stub(Session))],
        params: StatParams = Depends(),
) -> list[CampaignStatSchema]:
    if not params.groupby:
        expression = select(
            CampaignStat.date,
            CampaignStat.channel,
            CampaignStat.country,
            CampaignStat.os,
            CampaignStat.impressions,
            CampaignStat.clicks,
            CampaignStat.installs,
            CampaignStat.spend,
            CampaignStat.revenue,
            (CampaignStat.spend / CampaignStat.installs).label('cpi'),
        )
    else:
        columns = []
        fields = dict(zip(params.groupby, range(len(params.groupby))))
        for field in SORT_FIELDS_MAPPING:
            if field in fields:
                column = SORT_FIELDS_MAPPING[field]
            else:
                column = null().label(field)
            columns.append(column)

        expression = select(
            # func.row_number().over().label('id'),

            # null().label("date"),
            # null().label("channel"),
            # null().label("country"),
            # null().label("os"),
            *columns,

            func.sum(CampaignStat.impressions).label('impressions'),
            func.sum(CampaignStat.clicks).label('clicks'),
            func.sum(CampaignStat.installs).label('installs'),
            func.sum(CampaignStat.spend).label('spend'),
            func.sum(CampaignStat.revenue).label('revenue'),
            (CampaignStat.spend / CampaignStat.installs).label('cpi'),
        ).group_by(*params.groupby)

    if params.date_from:
        date_from: date = datetime.strptime(params.date_from, '%d-%m-%Y').date()
        expression = expression.where(CampaignStat.date >= date_from)
    if params.date_to:
        date_to: date = datetime.strptime(params.date_to, '%d-%m-%Y').date()
        expression = expression.where(CampaignStat.date < date_to)
    if params.channels:
        expression = expression.where(CampaignStat.channel.in_(params.channels))
    if params.countries:
        expression = expression.where(CampaignStat.country.in_(params.countries))
    if params.os:
        expression = expression.where(CampaignStat.os.in_(params.os))
    if params.sort:
        field = SORT_FIELDS_MAPPING.get(params.sort)
        if params.ordering == StatOrdering.asc:
            direction = asc
        else:
            direction = desc
        expression = expression.order_by(direction(field))

    stats = session.execute(expression).all()
    return stats

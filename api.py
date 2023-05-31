from typing import Annotated
from datetime import datetime, date

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, Column, desc, asc, func
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import null

from db_models import CampaignStat
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
        date_from: Annotated[str | None, Query()] = None,
        date_to: Annotated[str | None, Query()] = None,
        channels: Annotated[list[str] | None, Query()] = None,
        countries: Annotated[list[str] | None, Query()] = None,
        os: Annotated[list[str] | None, Query()] = None,
        sort: Annotated[str | None, Query()] = None,
        ordering: Annotated[str, Query()] = 'asc',
        groupby: Annotated[list[str] | None, Query()] = None,
) -> list[CampaignStatSchema]:

    if not groupby:
        expression = select(
            CampaignStat.id,
            CampaignStat.date,
            CampaignStat.channel,
            CampaignStat.country,
            CampaignStat.os,
            CampaignStat.impressions,
            CampaignStat.clicks,
            CampaignStat.installs,
            CampaignStat.spend,
            CampaignStat.revenue,
        )
    else:
        columns = []
        fields = dict(zip(groupby, range(len(groupby))))
        for field in SORT_FIELDS_MAPPING:
            if field in fields:
                column = SORT_FIELDS_MAPPING[field]
            else:
                column = null().label(field)
            columns.append(column)

        expression = select(
            func.row_number().over().label('id'),

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
        ).group_by(*groupby)

    # TODO compare date just by <>
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
    if sort:
        field = SORT_FIELDS_MAPPING.get(sort)
        if ordering == 'asc':
            direction = asc
        else:
            direction = desc
        expression = expression.order_by(direction(field))

    stats = session.execute(expression).all()
    return stats

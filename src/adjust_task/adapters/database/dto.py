from datetime import date

from pydantic import BaseModel

from adjust_task.adapters.database.gateways import Money
from adjust_task.infrastructure.db_models import ColumnName


class CampaignStatsDTO(BaseModel):

    date: date | None
    channel: ColumnName | None
    country: ColumnName | None
    os: ColumnName | None
    impressions: int
    clicks: int
    installs: int
    spend: Money
    revenue: Money
    cpi: Money

    class Config:
        orm_mode = True

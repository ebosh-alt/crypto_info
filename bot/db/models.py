from typing import Optional

from pydantic import BaseModel


class Quote(BaseModel):
    price: float
    volume_24h: float
    volume_change_24h: float
    percent_change_1h: float
    percent_change_24h: float
    percent_change_7d: float
    percent_change_30d: float
    percent_change_60d: float
    percent_change_90d: float
    last_updated: str


class Coin(BaseModel):
    name: str
    symbol: str
    quote: Optional[Quote] = None




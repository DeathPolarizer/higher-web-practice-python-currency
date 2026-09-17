from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class CurrencyDTO(BaseModel):
    id: int
    char_code: str
    num_code: str
    name: str
    nominal: int

    model_config = {"from_attributes": True}


class ExchangeRateDTO(BaseModel):
    id: int
    currency_id: int
    rate: Decimal
    date: date

    model_config = {"from_attributes": True}

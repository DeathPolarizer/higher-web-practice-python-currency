from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import CurrencyNotFoundError
from domain.currency.models import Currency, ExchangeRate


class CurrencyService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_currencies(self) -> list[Currency]:
        result = await self.db.execute(
            select(Currency).order_by(Currency.char_code)
        )
        return list(result.scalars().all())

    async def get_latest_rate(self, target_code: str) -> ExchangeRate:
        currency = await self._get_currency(target_code)
        result = await self.db.execute(
            select(ExchangeRate)
            .where(ExchangeRate.currency_id == currency.id)
            .order_by(ExchangeRate.date.desc())
            .limit(1)
        )
        rate = result.scalar_one_or_none()
        if rate is None:
            raise CurrencyNotFoundError(f"No rates found for {target_code}")
        return rate

    async def get_rate_history(
        self,
        target_code: str,
        start_date: date,
        end_date: date,
    ) -> list[ExchangeRate]:
        currency = await self._get_currency(target_code)
        result = await self.db.execute(
            select(ExchangeRate)
            .where(
                ExchangeRate.currency_id == currency.id,
                ExchangeRate.date >= start_date,
                ExchangeRate.date <= end_date,
            )
            .order_by(ExchangeRate.date)
        )
        return list(result.scalars().all())

    async def get_rates_for_currency(
        self, target_code: str
    ) -> list[ExchangeRate]:
        currency = await self._get_currency(target_code)
        result = await self.db.execute(
            select(ExchangeRate)
            .where(ExchangeRate.currency_id == currency.id)
            .order_by(ExchangeRate.date)
        )
        return list(result.scalars().all())

    async def _get_currency(self, char_code: str) -> Currency:
        result = await self.db.execute(
            select(Currency).where(Currency.char_code == char_code.upper())
        )
        currency = result.scalar_one_or_none()
        if currency is None:
            raise CurrencyNotFoundError(f"Currency {char_code} not found")
        return currency

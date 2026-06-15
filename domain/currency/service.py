from domain.currency.models import Currency, ExchangeRate
from datetime import date


class CurrencyService:
    async def list_currencies(self) -> list[Currency]:
        """Получить все доступные валюты.

        :return: Список всех объектов валют
        """
        raise NotImplementedError

    async def get_latest_rate(self, target_code: str) -> ExchangeRate | None:
        """Получить последний курс обмена для определенной валюты.

        :param target_code: Код валюты (например, 'USD', 'EUR')
        :return: Последний объект курса обмена или None если не найден
        """
        raise NotImplementedError

    async def get_rate_history(
        self,
        target_code: str,
        start_date: date,
        end_date: date,
    ) -> list[ExchangeRate]:
        """Получить исторические курсы обмена для определенной валюты.

        :param target_code: Код валюты (например, 'USD', 'EUR')
        :param start: Дата начала в формате YYYY-MM-DD
        :param end: Дата окончания в формате YYYY-MM-DD
        :return: Список объектов курса обмена за указанный период
        """
        raise NotImplementedError

    async def get_rates_for_currency(self, target_code: str) -> list[ExchangeRate]:
        """Получить все курсы обмена для определенной валюты (полная история).

        :param target_code: Код валюты (например, 'USD', 'EUR')
        :return: Список всех объектов курса обмена для валюты
        """
        raise NotImplementedError

from datetime import date, timedelta

import scrapy

from parser.items import CurrencyRateItem

URL_TEMPLATE = (
    "http://www.cbr.ru/scripts/XML_daily.asp?date_req={day}/{month}/{year}"
)

DAYS_TO_FETCH = 7


class CbrSpider(scrapy.Spider):
    name = "cbr"

    async def start(self):
        today = date.today()
        for i in range(DAYS_TO_FETCH):
            d = today - timedelta(days=i)
            url = URL_TEMPLATE.format(
                day=d.strftime("%d"),
                month=d.strftime("%m"),
                year=d.strftime("%Y"),
            )
            yield scrapy.Request(
                url,
                callback=self.parse,
                errback=self.errback,
                meta={"rate_date": d.isoformat()},
            )

    def parse(self, response):
        rate_date = response.meta["rate_date"]
        self.logger.info(
            f"Parsing rates for {rate_date}, status={response.status}, size={len(response.body)}"
        )

        for valute in response.xpath("//Valute"):
            raw_value = valute.xpath("Value/text()").get("0").replace(",", ".")
            try:
                rate = float(raw_value)
            except ValueError:
                continue

            item = CurrencyRateItem(
                char_code=valute.xpath("CharCode/text()").get("").strip(),
                num_code=valute.xpath("NumCode/text()").get("").strip(),
                name=valute.xpath("Name/text()").get("").strip(),
                nominal=int(valute.xpath("Nominal/text()").get("1")),
                rate=rate,
                date=rate_date,
            )
            yield item

    def errback(self, failure):
        self.logger.error(
            f"Request failed: {failure.request.url} — {failure.value.__class__.__name__}: {failure.value}"
        )

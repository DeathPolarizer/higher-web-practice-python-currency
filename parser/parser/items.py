import scrapy


class CurrencyRateItem(scrapy.Item):
    char_code = scrapy.Field()
    num_code = scrapy.Field()
    name = scrapy.Field()
    nominal = scrapy.Field()
    rate = scrapy.Field()
    date = scrapy.Field()

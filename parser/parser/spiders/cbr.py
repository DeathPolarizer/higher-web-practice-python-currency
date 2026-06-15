from scrapy import Spider


URL_TEMPLATE = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req={day}/{month}/{year}'

class CbrSpider(Spider):
    name = 'cbr'

    # TODO: реализовать скраппер для сайта ЦБ РФ

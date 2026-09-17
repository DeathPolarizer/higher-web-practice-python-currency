BOT_NAME = "parser"

SPIDER_MODULES = [f"{BOT_NAME}.spiders"]
NEWSPIDER_MODULE = [SPIDER_MODULES]

ADDONS = {}

ROBOTSTXT_OBEY = False

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 1
DOWNLOAD_TIMEOUT = 30

ITEM_PIPELINES = {
    "parser.pipelines.DatabasePipeline": 300,
}

FEED_EXPORT_ENCODING = "utf-8"

DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
}

# Follow HTTP → HTTPS redirects
REDIRECT_ENABLED = True
REDIRECT_MAX_TIMES = 5

LOG_LEVEL = "INFO"

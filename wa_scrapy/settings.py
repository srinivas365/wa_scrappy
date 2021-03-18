# Scrapy settings for wa_scrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'wa_scrapy'

SPIDER_MODULES = ['wa_scrapy.spiders',
                'wa_scrapy.spiders.amodelrecommends',
                'wa_scrapy.spiders.sephora',
                'wa_scrapy.spiders.healthline',
                'wa_scrapy.spiders.poshbeauty',
                "wa_scrapy.spiders.lorealparis",
                "wa_scrapy.spiders.fashionlady",
                "wa_scrapy.spiders.reallyree",
                "wa_scrapy.spiders.fleurdeforce",
                "wa_scrapy.spiders.hairbuddha",
                "wa_scrapy.spiders.hairducation",
                "wa_scrapy.spiders.hypehair",
                "wa_scrapy.spiders.lisaeldridge",
                "wa_scrapy.spiders.olapexblog",
                "wa_scrapy.spiders.viviscal",
                "wa_scrapy.spiders.carolinehirons",
                "wa_scrapy.spiders.richfeel",
                "wa_scrapy.spiders.matrixhair",
                "wa_scrapy.spiders.luxyhair",
                "wa_scrapy.spiders.theannaedit"
                ]
NEWSPIDER_MODULE = 'wa_scrapy.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'wa_scrapy (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'wa_scrapy.middlewares.WaScrapySpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'wa_scrapy.middlewares.WaScrapyDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'wa_scrapy.pipelines.WaScrapyPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


SELENIUM_DRIVER_NAME = 'chrome'
SELENIUM_DRIVER_EXECUTABLE_PATH = 'chromedriver.exe'
SELENIUM_DRIVER_ARGUMENTS=['--headless','--no-sandbox','--disable-gpu']  # '--headless' if using chrome instead of firefox

DOWNLOADER_MIDDLEWARES = {
    # 'scrapy_splash.SplashCookiesMiddleware': 723,
    # 'scrapy_splash.SplashMiddleware': 725,
    'scrapy_selenium.SeleniumMiddleware': 800,
    #'scrapy.downloadermiddlewares.robotstxt': None,
}

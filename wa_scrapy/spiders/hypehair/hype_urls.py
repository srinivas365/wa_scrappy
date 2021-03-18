import scrapy
from scrapy_selenium import SeleniumRequest

class HypeUrls(scrapy.Spider):
    name="hype_urls"

    # start_urls=["https://hypehair.com/haircare/",
    #             "https://hypehair.com/beauty/makeup/",
    #             "https://hypehair.com/beauty/skin/"
    #             ]

    # define custom mongodb output
    custom_settings = {

        # For mongodb Support with URL as primary key in item

        "ITEM_PIPELINES" : {
            "wa_scrapy.pipelines.MongoPipeline":500 
        },
        "MONGODB_SERVER" : "localhost:27017",
        "MONGODB_DB" : "hypehair",
        "OUTPUT_COLLECTION" : "urls"
    }

    def start_requests(self):
        urls=["https://hypehair.com/haircare/",
                "https://hypehair.com/beauty/makeup/",
                "https://hypehair.com/beauty/skin/"
                ]
        for url in urls:
            yield SeleniumRequest(url=url, callback=self.parse)


    def parse(self, response, **kwargs):
        for article_url in response.css('h4.elementor-post__title a::attr(href)').getall():
            yield {
                'url': article_url
            }

        next_page = response.css('a.page-numbers.next::attr(href)').get()
        if next_page is not None:
            yield SeleniumRequest(url=next_page, callback=self.parse)
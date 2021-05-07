import scrapy
from scrapy_selenium import SeleniumRequest
class CsUrls(scrapy.Spider):
    name="cs_urls"

    start_urls=["https://www.containerstore.com/organization-projects"]

    # define custom mongodb output
    custom_settings = {

        # For mongodb Support with URL as primary key in item

        "ITEM_PIPELINES" : {
            "wa_scrapy.pipelines.MongoPipeline":500 
        },
        "MONGODB_SERVER" : "mongodb://root:root@35.232.97.0:31400/?authSource=admin",
        "MONGODB_DB" : "containerstore",
        "OUTPUT_COLLECTION" : "urls",
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url,callback=self.parse)


    def parse(self, response, **kwargs):
        main_url="https://www.containerstore.com"
        for article_url in response.css('a.resource-card__wrapper::attr(href)').getall():
            yield {
                'url': main_url+article_url
            }


        next_page = response.css('a.block block__arrow.block__arrow--right::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
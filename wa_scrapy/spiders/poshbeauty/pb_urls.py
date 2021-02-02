import scrapy

class PbUrls(scrapy.Spider):
    name="pb_urls"

    start_urls=["http://www.poshbeautyblog.com/makeup",
                "http://www.poshbeautyblog.com/skincare",
                "http://www.poshbeautyblog.com/nails",
                "http://www.poshbeautyblog.com/hair"
               ]

    # define custom mongodb output
    custom_settings = {

        # For mongodb Support with URL as primary key in item

        "ITEM_PIPELINES" : {
            "wa_scrapy.pipelines.MongoPipeline":500 
        },
        "MONGODB_SERVER" : "localhost:27017",
        "MONGODB_DB" : "poshbeautyblog",
        "OUTPUT_COLLECTION" : "urls"
    }


    def parse(self, response, **kwargs):
        for article_url in response.css('div.more a::attr(href)').getall():
            article_url="http://www.poshbeautyblog.com"+article_url
            yield {
                'url': article_url
            }

        # next_page = response.css("div.nav-previous a:contains('Older')::attr(href)").get()
        next_page=response.xpath("//a[text()='Older']/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
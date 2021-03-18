import scrapy

class lisaUrls(scrapy.Spider):
    name="lisa_urls"

    start_urls=["https://www.lisaeldridge.com/blogs/articles/tagged/make-up",
                "https://www.lisaeldridge.com/blogs/articles/tagged/skincare"
                ]

    # define custom mongodb output
    custom_settings = {

        # For mongodb Support with URL as primary key in item

        "ITEM_PIPELINES" : {
            "wa_scrapy.pipelines.MongoPipeline":500 
        },
        "MONGODB_SERVER" : "localhost:27017",
        "MONGODB_DB" : "lisaeldridge",
        "OUTPUT_COLLECTION" : "urls"
    }


    def parse(self, response, **kwargs):

        for article_url in response.css('a.item::attr(href)').getall():
            article_url="https://www.lisaeldridge.com"+article_url
            yield {
                'url': article_url
            }

        # next_page = response.css('div.nav-previous a::attr(href)').get()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)
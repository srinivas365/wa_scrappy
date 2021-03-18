import scrapy

class VsUrls(scrapy.Spider):
    name="vs_urls"

    start_urls=["https://blog.viviscal.com/"]

    # define custom mongodb output
    custom_settings = {

        # For mongodb Support with URL as primary key in item

        "ITEM_PIPELINES" : {
            "wa_scrapy.pipelines.MongoPipeline":500 
        },
        "MONGODB_SERVER" : "localhost:27017",
        "MONGODB_DB" : "viviscal",
        "OUTPUT_COLLECTION" : "urls"
    }


    def parse(self, response, **kwargs):
        for article_url in response.css('h1.entry-title a::attr(href)').getall():
            yield {
                'url': article_url
            }

        next_page = response.css('a.nextpostslink::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
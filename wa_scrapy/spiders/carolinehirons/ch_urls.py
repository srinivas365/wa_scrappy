import scrapy

class ChUrls(scrapy.Spider):
    name="ch_urls"

    start_urls=["https://www.carolinehirons.com/page-category/skincare"]

    # define custom mongodb output
    custom_settings = {

        # For mongodb Support with URL as primary key in item

        "ITEM_PIPELINES" : {
            "wa_scrapy.pipelines.MongoPipeline":500 
        },
        "MONGODB_SERVER" : "localhost:27017",
        "MONGODB_DB" : "carolinehirons",
        "OUTPUT_COLLECTION" : "urls"
    }


    def parse(self, response, **kwargs):
        for article_url in response.css('h2.entry-title.p_post_titles_font a::attr(href)').getall():
            yield {
                'url': article_url
            }


        next_page = response.css('div.nav-previous a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
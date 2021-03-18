import scrapy

class ObUrls(scrapy.Spider):
    name="ob_urls"

    start_urls=["https://olaplex.com/blogs/news/"]

    # define custom mongodb output
    custom_settings = {

        # For mongodb Support with URL as primary key in item

        "ITEM_PIPELINES" : {
            "wa_scrapy.pipelines.MongoPipeline":500 
        },
        "MONGODB_SERVER" : "localhost:27017",
        "MONGODB_DB" : "olapexblog",
        "OUTPUT_COLLECTION" : "urls"
    }


    def parse(self, response, **kwargs):

        for article_url in response.css('div.blog-highlight__content a.text-btn.text-btn--small.arrow::attr(href)').getall():
            article_url="https://olaplex.com"+article_url
            yield {
                'url': article_url
            }

        next_page = response.css('a.pagination__next.pagination__item::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
import scrapy

class RealReeUrls(scrapy.Spider):
    name="rr_urls"

    start_urls=[
                "https://reallyree.com/skin/",
                "https://reallyree.com/hair/",
                "https://reallyree.com/skin/",
               ]

    # define custom mongodb output
    custom_settings = {

        # For mongodb Support with URL as primary key in item

        "ITEM_PIPELINES" : {
            "wa_scrapy.pipelines.MongoPipeline":500 
        },
        "MONGODB_SERVER" : "localhost:27017",
        "MONGODB_DB" : "reallyree",
        "OUTPUT_COLLECTION" : "urls"
    }


    def parse(self, response, **kwargs):
        category=response.request.url.split("/")[3]        
        articles=response.css("div.post-wrapper article.post-item")
        for article in articles:
            article_url=article.css("a:first-child::attr(href)").get()
            if "/about" not in article_url:
                yield {
                    'url': article_url,
                    'category':category
                }

        # next_page = response.css("div.nav-previous a:contains('Older')::attr(href)").get()
        next_page = response.css('a.next.page-numbers::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
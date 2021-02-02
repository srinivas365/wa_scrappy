import scrapy

class FlUrls(scrapy.Spider):
    name="fl_urls"

    # start_urls=["https://www.fashionlady.in/category/beauty-tips/haircare/page/"]

    # define custom mongodb output
    custom_settings = {

        # For mongodb Support with URL as primary key in item

        # "ITEM_PIPELINES" : {
        #     "wa_scrapy.pipelines.MongoPipeline":500 
        # },
        # "MONGODB_SERVER" : "localhost:27017",
        # "MONGODB_DB" : "amodelrecommends",
        # "OUTPUT_COLLECTION" : "urls"
    }


    def start_requests(self):
        urls=[
                {
                    "url":"https://www.fashionlady.in/category/beauty-tips/haircare/page/",
                    "min":1,
                    "max":28
                },
                {
                    "url":"https://www.fashionlady.in/category/beauty-tips/makeup/page/",
                    "min":1,
                    "max":33
                },
                {
                    "url":"https://www.fashionlady.in/category/beauty-tips/nail-care/page/",
                    "min":1,
                    "max":11
                },
                {
                    "url":"https://www.fashionlady.in/category/beauty-tips/skin-care/page/",
                    "min":1,
                    "max":18
                },
                {
                    "url":"https://www.fashionlady.in/category/health-tips/food-and-nutrition/page/",
                    "min":1,
                    "max":5
                },
                {
                    "url":"https://www.fashionlady.in/category/health-tips/home-remedies/page/",
                    "min":1,
                    "max":6
                },
                {
                    "url":"https://www.fashionlady.in/category/health-tips/weight-loss/page/",
                    "min":1,
                    "max":5
                },
            ]


        for cat in urls:
            for i in range(cat['min'],cat['max']):
                url=cat['url']+str(i)
                yield scrapy.Request(url=url,callback=self.parse)


    def parse(self, response, **kwargs):
        for article_url in response.css('div.td-read-more a::attr(href)').getall():
            yield {
                'url': article_url
            }


        next_page = response.css('div.nav-previous a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
import scrapy

class LorealUrls(scrapy.Spider):
    name="loreal_urls"

    # start_urls=["https://www.lorealparisusa.com/beauty-magazine/makeup.aspx?page=1",
    #             "https://www.lorealparisusa.com/beauty-magazine/hair-style.aspx?page=1",
    #             "https://www.lorealparisusa.com/beauty-magazine/hair-color.aspx?page=1",
    #             "https://www.lorealparisusa.com/beauty-magazine/skin-care.aspx?page=1"]

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
                    "url":"https://www.lorealparisusa.com/beauty-magazine/makeup.aspx?page=",
                    "min":1,
                    "max":212
                },
                {
                    "url":"https://www.lorealparisusa.com/beauty-magazine/hair-style.aspx?page=",
                    "min":1,
                    "max":104
                },
                {
                    "url":"https://www.lorealparisusa.com/beauty-magazine/hair-color.aspx?page=",
                    "min":1,
                    "max":94
                },
                {
                    "url":"https://www.lorealparisusa.com/beauty-magazine/skin-care.aspx?page=",
                    "min":1,
                    "max":224
                }

            ]


        for cat in urls:
            for i in range(cat['min'],cat['max']):
                url=cat['url']+str(i)
                yield scrapy.Request(url=url,callback=self.parse)
            
    def parse(self, response, **kwargs):
        for article_url in response.css('div.bm-article__caption a.js-article-cta::attr(href)').getall():
            article_url="https://www.lorealparisusa.com"+article_url
            yield {
                'url':article_url
            }


        # next_page = response.css('div.nav-previous a::attr(href)').get()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)
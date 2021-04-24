import scrapy

class SephFragUrls(scrapy.Spider):
    name="seph_frag_urls"

    start_urls=["https://community.sephora.com/t5/Fragrance-Fans/bd-p/perfume-posse?pageNum=1",]

    # define custom mongodb output
    custom_settings = {

        # For mongodb Support with URL as primary key in item

        "ITEM_PIPELINES" : {
            "wa_scrapy.pipelines.MongoPipeline":500 
        },
        "MONGODB_SERVER" : "localhost:27017",
        "MONGODB_DB" : "sephora",
        "OUTPUT_COLLECTION" : "frag_urls"
    }


    def parse(self, response, **kwargs):

        url = response.request.url
        page_num = int(url.split("=")[1])+1

        main_url="https://community.sephora.com"

        for article_url in response.css("div.reply-message-wrapper a.message-subject::attr(href)").getall():
            yield {
                'url': main_url+article_url
            }

        for article_url in response.css("div.post a.message-subject::attr(href)").getall():
            yield {
                'url': main_url+article_url
            }

        # next_page = response.css("div.nav-previous a:contains('Older')::attr(href)").get()
        next_page = response.css('a[aria-label="Next Page"]::attr(href)').get()
        if next_page is not None:
            next_url=url.split("=")[0]+"="+str(page_num)
            yield scrapy.Request(next_url,callback=self.parse)
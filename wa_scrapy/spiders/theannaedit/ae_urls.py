# https://www.matrix.com/api/blog/getblogs?itemid=%7B48C56F3E-0F05-4505-9181-9FE7FD743A1E%7D&ItemsPerPage=9&imageResizeKey=&showEmailSubscribeTile=1&Page=1&filter=&tilecount=0

import json
import scrapy
from pprint import pprint

class AnnaEditUrls(scrapy.Spider):
    name="ae_urls"
    download_delay = 1.5
    temp_url="https://www.theannaedit.com/category/beauty/page/{}/?_=1615725063845"
    
    start_urls=["https://www.theannaedit.com/category/beauty/page/1/?_=1615725063845",]

    # define custom mongodb output
    custom_settings = {
        # For mongodb Support with URL as primary key in item

        "ITEM_PIPELINES" : {
            "wa_scrapy.pipelines.MongoPipeline":500 
        },
        "MONGODB_SERVER" : "localhost:27017",
        "MONGODB_DB" : "theannaedit",
        "OUTPUT_COLLECTION" : "urls"
    }

    def parse(self, response, **kwargs):
        url=response.request.url
        
        if url.find("page/")==-1:
            next_page_no=2
        else:
            page_no=url.split("page/")[1].split("/")[0]
            next_page_no=int(page_no)+1
        links=response.css("a.the-post.text-center::attr(href)").getall()

        for link in links:
            yield {"url":link}

        if links!=[]:
            next_url=self.temp_url.format(next_page_no)
            yield scrapy.Request(url=next_url, callback=self.parse)
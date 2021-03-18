# https://www.matrix.com/api/blog/getblogs?itemid=%7B48C56F3E-0F05-4505-9181-9FE7FD743A1E%7D&ItemsPerPage=9&imageResizeKey=&showEmailSubscribeTile=1&Page=1&filter=&tilecount=0

import json
import scrapy
from pprint import pprint

class LuxyUrls(scrapy.Spider):
    name="luxy_urls"
    download_delay = 1.5
    temp_url="https://www.luxyhair.com/blogs/hair-blog/tagged/hair-care-advice?view=thumbnails&page={}"
    
    start_urls=["https://www.luxyhair.com/blogs/hair-blog/tagged/hair-care-advice?view=thumbnails&page=1",]

    # define custom mongodb output
    custom_settings = {
        # For mongodb Support with URL as primary key in item

        "ITEM_PIPELINES" : {
            "wa_scrapy.pipelines.MongoPipeline":500 
        },
        "MONGODB_SERVER" : "localhost:27017",
        "MONGODB_DB" : "luxyhair",
        "OUTPUT_COLLECTION" : "urls"
    }

    def parse(self, response, **kwargs):
        page_no=response.request.url.split("=")[-1]
        next_page_no=int(page_no)+1
        links=response.css("a.image-container.local--image-container::attr(href)").getall()
        for link in links:
            link="https://www.luxyhair.com"+link
            yield {"url":link}

        if links!=[]:
            next_url=self.temp_url.format(next_page_no)
            yield scrapy.Request(url=next_url, callback=self.parse)
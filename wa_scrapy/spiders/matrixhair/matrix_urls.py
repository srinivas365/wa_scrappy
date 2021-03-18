# https://www.matrix.com/api/blog/getblogs?itemid=%7B48C56F3E-0F05-4505-9181-9FE7FD743A1E%7D&ItemsPerPage=9&imageResizeKey=&showEmailSubscribeTile=1&Page=1&filter=&tilecount=0

import json
import scrapy
from pprint import pprint

class MatrixUrls(scrapy.Spider):
    name="matrix_urls"
    download_delay = 1.5

    start_urls=["https://www.matrix.com/api/blog/getblogs?itemid=%7B48C56F3E-0F05-4505-9181-9FE7FD743A1E%7D&ItemsPerPage=9&imageResizeKey=&showEmailSubscribeTile=1&Page=0&filter=&tilecount=0",
                ]

    # define custom mongodb output
    custom_settings = {
        "ROBOTSTXT_OBEY":"False",
        # For mongodb Support with URL as primary key in item

        "ITEM_PIPELINES" : {
            "wa_scrapy.pipelines.MongoPipeline":500 
        },
        "MONGODB_SERVER" : "localhost:27017",
        "MONGODB_DB" : "matrixhair",
        "OUTPUT_COLLECTION" : "urls"
    }


    def parse(self, response, **kwargs):
        temp_url="https://www.matrix.com/api/blog/getblogs?itemid=%7B48C56F3E-0F05-4505-9181-9FE7FD743A1E%7D&ItemsPerPage=9&imageResizeKey=&showEmailSubscribeTile=1&Page={}&filter=&tilecount=0"
        url=response.request.url
        page=url.split("&Page=")
        page_no=page[1].split("&")[0]
        next_pag_no=int(page_no)+1

        data = json.loads(response.body)

        blogs_data=data['Data']['Results']
        for blog in blogs_data:
            yield {
                "url":blog['BlogLink']
            }

        if data['Data']['IsLastPage']!=True:
            next_url=temp_url.format(next_pag_no)
            yield scrapy.Request(url=next_url, callback=self.parse)
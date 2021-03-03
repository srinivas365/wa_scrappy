"""Takes list of URLS from file and scrape the data from the each URL."""
from scrapy.loader import ItemLoader
from wa_scrapy.items import SephoraHtmlItem
import scrapy
import json
from pymongo import MongoClient


class SephoraCrawler(scrapy.Spider):
    """Takes list of URLS from file and scrape the data from the each URL."""
    name = "sephora_crawler"

    custom_settings = {
        "ITEM_PIPELINES" : {
            "wa_scrapy.pipelines.MongoPipeline":500 
        },
        "MONGODB_SERVER" : "localhost:27017",
        "MONGODB_DB" : "sephora",
        "OUTPUT_COLLECTION" : "posts_html_v2"
    }
    
    def start_requests(self):
        client = MongoClient(self.settings["MONGODB_SERVER"])
        mongo_db = client[self.settings["MONGODB_DB"]]
        output_collection = mongo_db[self.settings["OUTPUT_COLLECTION"]]
        with open(self.file) as file:
            links = json.load(file)

            for link in links[:1000]:
                url=link['url']

                if self.force == "True":
                    yield scrapy.Request(url=url, callback=self.parse)
                else:  # force = false, don't force if it's already present
                    if output_collection.find_one({"url": url}):
                        self.logger.info("already scraped")
                    else:
                        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        post_url=response.request.url
        x=post_url.split("/")
        if post_url.find("page")!=-1:
            post_id=x[-3]
        else:
            post_id=x[-1]


        loader = ItemLoader(item=SephoraHtmlItem(), selector=response)
        loader.add_value("url",post_url)
        loader.add_value("post_id",post_id)
        loader._add_value("content",response.body.decode('utf-8'))
        # yield {
        #     "url":response.request.url,
        #     "post_id":post_id,
        #     "content":response.body.decode('utf-8')
        # }

        yield loader.load_item()

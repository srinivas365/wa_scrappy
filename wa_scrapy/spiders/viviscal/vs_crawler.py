"""Takes list of URLS from file and scrape the data from the each URL."""
import scrapy
import json
from pymongo import MongoClient


class VsCrawler(scrapy.Spider):
    """Takes list of URLS from file and scrape the data from the each URL."""
    name = "vs_crawler"

    custom_settings = {
        "ITEM_PIPELINES" : {
            "wa_scrapy.pipelines.MongoPipeline":500 
        },
        "MONGODB_SERVER" : "localhost:27017",
        "MONGODB_DB" : "viviscal",
        "OUTPUT_COLLECTION" : "vs_html"
    }
    
    def start_requests(self):
        client = MongoClient(self.settings["MONGODB_SERVER"])
        mongo_db = client[self.settings["MONGODB_DB"]]
        output_collection = mongo_db[self.settings["OUTPUT_COLLECTION"]]
        with open(self.file) as file:
            links = json.load(file)

            for link in links:
                url=link['url']

                if self.force == "True":
                    yield scrapy.Request(url=url, callback=self.parse)
                else:  # force = false, don't force if it's already present
                    if output_collection.find_one({"url": url}):
                        self.logger.info("already scraped")
                    else:
                        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        yield {
            "url":response.request.url,
            "content":response.body.decode('utf-8')
        }

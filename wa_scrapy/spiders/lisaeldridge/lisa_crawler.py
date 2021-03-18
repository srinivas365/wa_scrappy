"""Takes list of URLS from file and scrape the data from the each URL."""
import scrapy
import json
from pymongo import MongoClient
from scrapy_selenium import SeleniumRequest


class LisaCrawler(scrapy.Spider):
    """Takes list of URLS from file and scrape the data from the each URL."""
    name = "lisa_crawler"

    custom_settings = {
        "ITEM_PIPELINES" : {
            "wa_scrapy.pipelines.MongoPipeline":500 
        },
        "MONGODB_SERVER" : "localhost:27017",
        "MONGODB_DB" : "lisaeldridge",
        "OUTPUT_COLLECTION" : "lisa_html",
        "DOWNLOAD_DELAY":3,
        "AUTOTHROTTLE_ENABLED" : True,
        "AUTOTHROTTLE_START_DELAY" : 1,
        "AUTOTHROTTLE_MAX_DELAY" : 3
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

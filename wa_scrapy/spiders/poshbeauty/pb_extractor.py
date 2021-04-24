""" To extract from raw HTML content"""
from pickle import load
from wa_scrapy.items import PoshBeautyItem
import scrapy
from pymongo import MongoClient
from scrapy.utils.project import get_project_settings
from scrapy.loader import ItemLoader
import os
settings=get_project_settings()


class PbExtractor(scrapy.Spider):
    """ To scrape the ingredients from EWG"""
    name = "pb_extractor"
    
    custom_settings = {
        "ROBOTSTXT_OBEY":"False",
        "ITEM_PIPELINES" : {
            "wa_scrapy.pipelines.MongoPipeline":500 
        },
        "MONGODB_SERVER" : "localhost:27017",
        "MONGODB_DB" : "poshbeautyblog",
        "INPUT_COLLECTION" : "pb_html",
        "OUTPUT_COLLECTION":"pb_articles_v2"
    }
    
    def start_requests(self):
        # don't edit this 
        client = MongoClient(self.settings["MONGODB_SERVER"])
        mongo_db = client[self.settings["MONGODB_DB"]]
        input_collection = mongo_db[self.settings["INPUT_COLLECTION"]]
        output_collection = mongo_db[self.settings["OUTPUT_COLLECTION"]]
        html_files = input_collection.find()

        print(input_collection.count_documents({}))
        for html_file in html_files:
            file_id=str(html_file["_id"])
            temp_file=f"temp_files/{file_id}.html"
            with open(f'./{temp_file}',"w",encoding="utf-8") as file:
                file.write(html_file["content"])
            url = f"file:///E:/wish-assimilation/scrapy_crawlers/wa_scrapy/{temp_file}"
            url_exist = output_collection.find_one({"url": html_file["url"]})
            if self.force == "True" or not url_exist:
                yield scrapy.Request(url=url, callback=self.parse,
                                     meta={"url": html_file["url"], "temp_file": temp_file})
            else:
                self.logger.info("URL has been extracted already")


    def parse(self, response):

        # edit this only
        url = response.meta.get('url')
        title = response.css("h1.post-title a::text").get()
        author = response.css("div.author::text").get() 
        categories = response.css("div.categories a::text").getall()
        tags = response.css("div.tags a::text").getall()
        date = response.css("time.published::text").get()  
        content = response.css("div.sqs-block-content p:not(:first-child) ::text").getall()
        content=' '.join(content[1:])

        loader = ItemLoader(item=PoshBeautyItem(), selector=response)
        loader.add_value("url",url)
        loader.add_value("author",author)
        loader.add_value("title",title)
        loader.add_value("categories",categories)
        loader.add_value("tags",tags)
        loader.add_value("date",date)
        loader.add_value("content",content)

        os.remove(response.meta.get('temp_file'))
        return loader.load_item()


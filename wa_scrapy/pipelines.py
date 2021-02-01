# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


""" Define your item pipelines here """
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
import logging
import pymongo
from scrapy.utils.project import get_project_settings
logger = logging.getLogger(__name__)
settings = get_project_settings()

class MongoPipeline:
    """To export the data to MongoDB"""


    def open_spider(self, spider):
        logger.info(dict(spider.settings))
        logger.info(spider.settings["MONGODB_SERVER"])
        logger.info(spider.settings["MONGODB_DB"])
        logger.info(spider.settings["OUTPUT_COLLECTION"])

        self.mongo_uri=spider.settings["MONGODB_SERVER"]
        self.mongo_db=spider.settings["MONGODB_DB"]

        self.client = pymongo.MongoClient(self.mongo_uri)
        self.database = self.client[self.mongo_db]
        self.collection=self.database[spider.settings["OUTPUT_COLLECTION"]]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.collection.update(
            {'url': item['url']}, dict(item), upsert=True)
        return item


    

""" To extract from raw HTML content"""
from pickle import load
from wa_scrapy.items import HealthlineArticleItem
import scrapy
from pymongo import MongoClient
from scrapy.utils.project import get_project_settings
from scrapy.loader import ItemLoader
import os
settings=get_project_settings()


class HealthlineExtractor(scrapy.Spider):
    """ To scrape the ingredients from EWG"""
    name = "healthline_extractor"
    
    custom_settings = {
        "ROBOTSTXT_OBEY":"False",
        "ITEM_PIPELINES" : {
            "wa_scrapy.pipelines.MongoPipeline":500 
        },
        # "MONGODB_SERVER" : "localhost:27017",
        "MONGODB_SERVER":"mongodb+srv://srinivas:loveudad@cluster0.traj4.mongodb.net/test?retryWrites=true&w=majority",
        "MONGODB_DB" : "healthline",
        "INPUT_COLLECTION" : "hl_html",
        "OUTPUT_COLLECTION":"hl_articles"
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
        # change the code here
        articles = response.xpath("//div[@data-article-body]")
        for article in articles:
            info = article.css(".css-jy1umg").xpath(".//text()").getall()
            article_info = ''.join(info)
            article_topics = article.css("div.css-0")
            topics = []
            for topic in article_topics[1:]:
                # content_loader = ItemLoader(
                #     item=HealthlineContentItem(), selector=topic)
                # content_loader.add_css("topic_name", "a::attr(name)")
                topic_data = topic.xpath(".//text()").getall()
                topic_data = ''.join(topic_data[1:])
                # content_loader.add_value("topic_data", topic_data)
                topics.append(topic_data)
            
            content=' '.join(topics)
            loader = ItemLoader(item=HealthlineArticleItem(), selector=article)
            loader.add_css("title", "h1::text")
            loader.add_value("url", response.meta.get('url'))
            loader.add_value("article_info", article_info)
            loader.add_value("content", content)
            os.remove(response.meta.get('temp_file'))
            yield loader.load_item()

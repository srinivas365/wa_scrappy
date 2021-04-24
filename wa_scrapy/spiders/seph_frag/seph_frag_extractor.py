""" To extract from raw HTML content"""
from pickle import load
from wa_scrapy.items import SephoraPost, SephoraReply
import scrapy
from pymongo import MongoClient
from scrapy.utils.project import get_project_settings
from scrapy.loader import ItemLoader
import os
settings=get_project_settings()


class SephFragExtractor(scrapy.Spider):
    """ To scrape the ingredients from EWG"""
    name = "seph_frag_extractor"
    
    custom_settings = {
        "ROBOTSTXT_OBEY":"False",
        "ITEM_PIPELINES" : {
            "wa_scrapy.pipelines.SephoraMongoPipeline":500 
        },
        "MONGODB_SERVER" : "localhost:27017",
        "MONGODB_DB" : "sephora",
        "INPUT_COLLECTION" : "frag_html",
        "OUTPUT_COLLECTION":"frag_posts"
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

            post_id=html_file["url"].split("/")[-1]

            if self.force == "True" or not url_exist:
                yield scrapy.Request(url=url, callback=self.parse,
                                     meta={"url": html_file["url"], "temp_file": temp_file, "post_id":post_id})
            else:
                self.logger.info("URL has been extracted already")


    def parse(self, response):

        # edit this only
        url = response.meta.get('url')
        post_id=response.meta.get('post_id')
        hearts_count=response.css("div.lia-kudos span.lia-count::text").get()
        views=response.css("div.lia-views span.lia-count::text").get()
        replies_count=response.css("div.lia-component-reply-count span.lia-count::text").get()
        time_details=response.css("time::attr(title)").getall() # posted and updated
        group=response.css("a.board::text").get() 
        title=response.css("h2.message-subject div.lia-message-subject::text").get()

        post={
            "data":'',
        }
        post_data=response.css("div.lia-threaded-detail-display-message-view")
        post["data"]=post_data[0].xpath(".//p//text()").getall()
        post["data"]=" ".join(post["data"])
        
        replies=[]
        product_urls=[]
        url_prefix="https://community.sephora.com"
        for reply in post_data[1:]:
            reply_data=reply.xpath(".//div[@class='lia-message-body-content']//text()").getall()
            reply_data=' '.join(reply_data)
            reply_loader=ItemLoader(item=SephoraReply(),selector=reply)
            reply_loader.add_value("reply",reply_data)
            cleaned_reply=dict(reply_loader.load_item())
            if "reply" in cleaned_reply.keys():
                replies.append(cleaned_reply["reply"])
            
            products=reply.css("ul.lia-product-list a::attr('href')").getall()
            if len(products) > 0:
                products=list(map(lambda x:url_prefix+x, products))
                product_urls.extend(products)


        loader = ItemLoader(item=SephoraPost(), selector=response)
        loader.add_value('url',url)
        loader.add_value('post_id', post_id)
        loader.add_value("title",title)
        loader.add_value("group",group)
        loader.add_value("time_details",time_details)
        loader.add_value("replies_count",replies_count)
        loader.add_value("views",views)
        loader.add_value("hearts_count",hearts_count)
        loader.add_value("content",post["data"])
        loader.add_value("replies",replies)
        loader.add_value("product_urls",product_urls)

        os.remove(response.meta.get('temp_file'))

        yield loader.load_item()


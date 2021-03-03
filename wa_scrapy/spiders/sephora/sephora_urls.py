import scrapy

class SephoraUrls(scrapy.Spider):
    name="sephora_urls"

    start_urls=["https://community.sephora.com/?pageNum=1"]

    # define custom mongodb output
    custom_settings = {

        # For mongodb Support with URL as primary key in item

        # "ITEM_PIPELINES" : {
        #     "wa_scrapy.pipelines.MongoPipeline":500 
        # },
        # "MONGODB_SERVER" : "localhost:27017",
        # "MONGODB_DB" : "amodelrecommends",
        # "OUTPUT_COLLECTION" : "urls"
    }


    def parse(self,response):
        
        posts=response.xpath("//div[@class='reply-message-wrapper']")

        for post in posts:
            post_link = post.css('a.message-subject::attr(href)').get()
            if post_link is not None:
                post_id=post_link.split("/")[-1]
                post_link="https://community.sephora.com"+post_link
                replies_count=int(post.css("span.replies-count::text").get())
                replies_count=(replies_count//21)+1
                for count in range(replies_count):
                    new_post_link=post_link+"/page/"+str(count)
                    yield {'url':new_post_link,"post_id":post_id}

        just_posts=response.xpath("//div[@class='message-block post']")
        for post in just_posts:
            post_link = post.css('a.message-subject::attr(href)').get()
            if post_link is not None:
                post_link="https://community.sephora.com"+post_link
                yield {'url':post_link}

        split_url=response.url.split("=")
        curr_page=split_url[1]

        next_page=int(curr_page)+1
        np="Page "+str(next_page)

        path=".//a[@aria-label='"+np+"']"
        next_rep=response.xpath(path).get()
        next_url=None
        if next_rep is not None:
            next_url=split_url[0]+"="+str(next_page)
            yield scrapy.Request(next_url,callback=self.parse)
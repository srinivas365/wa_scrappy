# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field
from scrapy.loader.processors import MapCompose, TakeFirst
import re

def to_lowercase(text):
    """To convert the data into lowercase"""

    return text.lower()

def remove_unicode_chars(text):
    # """ To remove the unicode character from the data"""
    # text=text.encode("utf-8",errors='ignore').decode("utf-8")
    # text=re.sub("https?:.*(?=\s)",'',text)
    # text=re.sub("’","'",text)
    # text=re.sub("[^\x00-\x7f]+",'',text)
    # text=re.sub('[?:#%<>,!@&\(\)\\n\\t;|$]','',text)
    # text=re.sub("  *",' ',text)
    # return text.strip()

    """ To remove the unicode character from the data"""
    text=text.encode("utf-8",errors='ignore').decode("utf-8")
    text=re.sub("https?:.*(?=\s)",'',text)
    text=re.sub("[’\"]","'",text)
    text=re.sub("[^\x00-\x7f]+",' ',text)
    text=re.sub('[#&\\()*+/:;<=>@[\]^_`{|}~ \t\n\r]',' ',text)
    # text=re.sub('[!"#&\\()*+,./:;<=>?@[\]^_`{|}~ \t\n\r]',' ',text)
    text=re.sub("  *",' ',text)
    return text.strip()

class AmrArticle(scrapy.Item):
    url=Field(output_processor=TakeFirst())
    content=Field(input_processor=MapCompose(to_lowercase,remove_unicode_chars),output_processor=TakeFirst())
    author=Field(output_processor=TakeFirst())
    title=Field(input_processor=MapCompose(to_lowercase,remove_unicode_chars),output_processor=TakeFirst())

class HealthlineArticleItem(scrapy.Item):
    """ Acts as JSON Object retrived from Healthline website that stores the article data"""
    title = Field(input_processor=MapCompose(to_lowercase,remove_unicode_chars),output_processor=TakeFirst())
    url = Field(output_processor=TakeFirst())
    article_info = Field(output_processor=TakeFirst())
    content=Field(input_processor=MapCompose(to_lowercase,remove_unicode_chars),output_processor=TakeFirst())

class SephoraPost(scrapy.Item):
    
    title=Field(input_processor=MapCompose(to_lowercase,remove_unicode_chars),output_processor=TakeFirst())
    group=Field(output_processor=TakeFirst())
    time_details=Field()
    replies_count=Field(output_processor=TakeFirst())
    views=Field(output_processor=TakeFirst())
    hearts_count=Field(output_processor=TakeFirst())
    post=Field(input_processor=MapCompose(to_lowercase,remove_unicode_chars),output_processor=TakeFirst())
    product_urls=Field()
    replies=Field()
    
class SephoraReply(scrapy.Item):
    reply=Field(input_processor=MapCompose(to_lowercase,remove_unicode_chars),output_processor=TakeFirst())

class LorealParisItem(scrapy.Item):
    url = Field(output_processor=TakeFirst())
    title = Field(input_processor=MapCompose(to_lowercase,remove_unicode_chars),output_processor=TakeFirst())
    category = Field(output_processor=TakeFirst())
    content = Field(input_processor=MapCompose(to_lowercase,remove_unicode_chars),output_processor=TakeFirst())

class FashionLadyItem(scrapy.Item):
    url = Field(output_processor=TakeFirst())
    title = Field(input_processor=MapCompose(to_lowercase,remove_unicode_chars),output_processor=TakeFirst())
    time = Field(output_processor=TakeFirst())
    content = Field(input_processor=MapCompose(to_lowercase,remove_unicode_chars),output_processor=TakeFirst())
 
class PoshBeautyItem(scrapy.Item):
    url = Field(output_processor=TakeFirst())
    title = Field(input_processor=MapCompose(to_lowercase,remove_unicode_chars),output_processor=TakeFirst())
    author = Field(input_processor=MapCompose(to_lowercase,remove_unicode_chars),output_processor=TakeFirst())
    categories = Field(input_processor=MapCompose(to_lowercase,remove_unicode_chars))
    tags = Field(input_processor=MapCompose(to_lowercase,remove_unicode_chars))
    date = Field(input_processor=MapCompose(to_lowercase,remove_unicode_chars),output_processor=TakeFirst())
    content = Field(input_processor=MapCompose(to_lowercase,remove_unicode_chars),output_processor=TakeFirst())

class SephoraPost(scrapy.Item):
    url = Field(output_processor=TakeFirst())
    post_id = Field(output_processor=TakeFirst())
    title=Field(input_processor=MapCompose(to_lowercase,remove_unicode_chars),output_processor=TakeFirst())
    group=Field(output_processor=TakeFirst())
    time_details=Field()
    replies_count=Field(output_processor=TakeFirst())
    views=Field(output_processor=TakeFirst())
    hearts_count=Field(output_processor=TakeFirst())
    content=Field(input_processor=MapCompose(to_lowercase,remove_unicode_chars),output_processor=TakeFirst())
    product_urls=Field()
    replies=Field()

    
class SephoraReply(scrapy.Item):
    reply=Field(input_processor=MapCompose(to_lowercase,remove_unicode_chars),output_processor=TakeFirst())

class SephoraHtmlItem(scrapy.Item):
    url = Field(output_processor=TakeFirst())
    post_id = Field(output_processor=TakeFirst())
    content=Field(output_processor=TakeFirst())

    def __repr__(self):
        return repr({"url":self["url"],"post_id":self["post_id"]})
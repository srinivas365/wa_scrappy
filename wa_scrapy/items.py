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
    """ To remove the unicode character from the data"""
    #text=text.encode("utf-8",errors='ignore').decode("utf-8")
    text=(text.encode('ascii', 'ignore')).decode('utf-8')
    text=re.sub("https?:.*(?=\s)",'',text)
    text=re.sub("’","'",text)
    text=re.sub(r"[^\x00-\x7f]+",'',text)
    text=re.sub('[?:#%<>,!@&\(\)\\n\\t;]','',text)
    text=re.sub("  *",' ',text)
    return text.strip()



class AmrArticle(scrapy.Item):
    url=Field(output_processor=TakeFirst())
    content=Field(input_processor=MapCompose(to_lowercase,remove_unicode_chars),output_processor=TakeFirst())
    author=Field(output_processor=TakeFirst())
    title=Field(input_processor=MapCompose(to_lowercase,remove_unicode_chars),output_processor=TakeFirst())


class HealthlineArticleItem(scrapy.Item):
    """ Acts as JSON Object retrived from Healthline website that stores the article data"""
    article_name = Field(output_processor=TakeFirst())
    url = Field(output_processor=TakeFirst())
    article_info = Field(output_processor=TakeFirst())
    content = Field()

    

class HealthlineContentItem(scrapy.Item):
    """Acts as JSON Object that stores the paragraph headings and paragraph content """
    topic_name = Field(input_processor=MapCompose(
        to_lowercase), output_processor=TakeFirst())
    topic_data = Field(input_processor=MapCompose(
        to_lowercase, remove_unicode_chars), output_processor=TakeFirst())
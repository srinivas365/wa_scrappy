"""Crawl through all pages of website having articles and scrape the data from each article."""
import scrapy

class HealthlineUrls(scrapy.Spider):
    """Crawl through all pages of website having articles and scrape the data from each article."""
    name = "healthline_urls"
    start_urls = ["https://www.healthline.com/directory/topics?page=0"]


    def parse(self, response):
        links = response.xpath("//ul//li[@class='css-12tk9my']//a")
        for link in links:
            link_url = link.attrib["href"]
            if self.tag in link_url:
                yield {"url":link_url}

        next_page = response.css('a.css-gnpdi1::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    
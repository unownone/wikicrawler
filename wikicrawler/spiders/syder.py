import scrapy
from wikicrawler.items import Wikipedia
from datetime import datetime
import re


class WikiCrawler(scrapy.Spider):
    name = 'wiki_crawler'
    BASE_URL = 'https://www.wikipedia.org'
    start_urls = ['https://en.wikipedia.org/wiki/Wikipedia:Contents/History_and_events']
    
    def parse(self,response):
        for href in response.css('.contentsPage__header,.contentsPage__section a::attr(href)'):
            url = self.BASE_URL + href.extract().strip()
            yield scrapy.Request(url, callback=self.parse_page)
            
    def parse_page(self,response):
        item = Wikipedia()
        item['title'] = response.css('.firstHeading::text').extract_first()
        item['url'] = response.url
        item['data'] = response.css('.mw-parser-output p::text').extract()
        yield item
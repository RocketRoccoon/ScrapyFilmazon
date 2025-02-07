import scrapy


class ScrapyfilmazoncrawlerSpider(scrapy.Spider):
    name = "ScrapyFilmazonCrawler"
    allowed_domains = ["filmazon.my"]
    start_urls = ["https://filmazon.my"]

    def parse(self, response):
        pass

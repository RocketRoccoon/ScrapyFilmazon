import scrapy
import re


class ScrapyfilmazoncrawlerSpider(scrapy.Spider):
    name = "MoviesFilmazonCrawler"
    allowed_domains = ["filmazon.my"]
    start_urls = ["https://filmazon.my/movie?sort=created_at_asc"]
    custom_settings = {
        # 'LOG_FILE': 'Filmazon1.log',
        # 'LOG_MODE': 'w',
        'CONCURRENT_REQUESTS': 64,
    }

    def parse(self, response):
        items = response.xpath("//section[contains(@class, 'site-posts')]/article")

        for item in items:
            link = item.xpath("./div/div/h2/a/@href").get()
            # link = response.urljoin(link)
            yield scrapy.Request(url=link, callback=self.parse_item)

        for i in range(2, 3):
            next_page = f'https://filmazon.my/movie?sort=created_at_asc&page={i}'
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_item(self, response):
        yield {
            'name': re.search(r'([A-Za-z\s:]+)\s\d{4}', response.xpath('//h1[@class="title"]/text()').get()).group(1).strip(),
            'genre': (lambda genres: ", ".join(genres) if genres else "No info")(response.xpath('//i[contains(@class, "fa-light fa-masks-theater")]/../following-sibling::div/a/text()').getall()),
            'release_year': (lambda : response.xpath('//i[contains(@class, "fa-light fa-calendar-day")]/../following-sibling::div/a/text()').get() or "no info")(),
            'duration': (lambda : re.findall(r'\d+', response.xpath('//i[contains(@class, "fa-light fa-alarm-clock")]/../following-sibling::div/a/text()').get())[0] if response.xpath('//i[contains(@class, "fa-light fa-alarm-clock")]/../following-sibling::div/a/text()').get() else "no info")(),
            'age_rating': (lambda : response.xpath('//i[contains(@class, "fa-light fa-user-plus")]/../following-sibling::div/a/text()').get() or "no info")(),
            'imdb_score': (lambda: response.xpath("//div[contains(@class, 'item imdb')]/div/div/span/text()").get() or "no info")(),
            'imdb_votes': (lambda: response.xpath("//div[contains(@class, 'imdb')]/div/div/small/text()").get() or "no info")(),
            'meta_score': (lambda: (match.group(1) if (match := re.search(r'(\d+)/\d+', response.xpath("//div[contains(@class, 'metacritic')]/div/div/span/text()").get() or "")) else "no info"))(),
            'rotten_tomatoes': (lambda: (match.group(1) if (match := re.search(r'(\d+)%', response.xpath("//div[contains(@class, 'rotten')]/div/div/span/text()").get() or "")) else "no info"))(),
            'director': (lambda directors: ", ".join(directors) if directors else "No info")(response.xpath('//i[contains(@class, "fa-light fa-camera-movie")]/../following-sibling::div/a/text()').getall()),
            'star1': (lambda : response.xpath('//i[contains(@class, "fa-light fa-users")]/../following-sibling::div/a[1]/text()').get() or "no info")(),
            'star2': (lambda : response.xpath('//i[contains(@class, "fa-light fa-users")]/../following-sibling::div/a[2]/text()').get() or "no info")(),
            'star3': (lambda : response.xpath('//i[contains(@class, "fa-light fa-users")]/../following-sibling::div/a[3]/text()').get() or "no info")(),
            'country': (lambda countries: ", ".join(countries) if countries else "No info")(response.xpath('//i[contains(@class, "fa-light fa-earth-americas")]/../following-sibling::div/a/text()').getall()),
            'language': (lambda languages: ", ".join(languages) if languages else "No info")(response.xpath('//i[contains(@class, "fa-light fa-globe")]/../following-sibling::div/a/text()').getall()),
            'download_counts': (lambda lst: sum(map(int, lst)) if lst else "no info")(response.xpath('//span[contains(@class, "download-number")]/text()').getall()),
            'number_of_comments': (lambda: response.xpath("//div[contains(@class, 'title')]/span[contains(@class,'count')]/text()").get() or "no info")(),
            'description': (lambda: response.xpath("//p[contains(@class, 'post-excerpt')]/text()").get() or "no info")()
        }
#         //section[contains(@class, 'postbox-information')]/div[contains(@class, 'postbox-sec')]/div/div/div/div[contains(@class, 'links-main')]/div/div/div/span[contains(@class, 'download-number')]/text()



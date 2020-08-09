import scrapy
from scrapy.http import HtmlResponse
from leroy.items import LeroyItem
from scrapy.loader import ItemLoader

class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        super().__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//div[@class='next-paginator-button-wrapper']/a/@href").extract_first()
        items_title_links = response.xpath("//a[@slot='name']/@href").extract()
        for link in items_title_links:
            yield response.follow(link, callback=self.parse_items)

        if next_page:
            yield response.follow(next_page, callback=self.parse_items)
        pass

    def parse_items(self, response:HtmlResponse):
        loader = ItemLoader(item=LeroyItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('photos', "//source[@media=' only screen and (min-width: 1024px)']/@srcset")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_value('url', response.url)
        loader.add_xpath('keys_chars', "//dl[@class='def-list']//dt//text()")
        loader.add_xpath('values_chars', "//dl[@class='def-list']//dd/text()")
        yield loader.load_item()

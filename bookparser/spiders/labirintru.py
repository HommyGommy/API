import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem

class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D0%B1%D1%83%D0%BB%D0%B3%D0%B0%D0%BA%D0%BE%D0%B2/']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//div[@class='pagination-next']//a[@class='pagination-next__text']/@href").extract_first()
        book_title_links = response.xpath("//a[@class='product-title-link']/@href").extract()
        for link in book_title_links:
            yield response.follow(link, callback=self.book_parse)

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response:HtmlResponse):
        link = response.url
        name = response.xpath("//h1/text()").extract_first()
        author = response.xpath("//div[@class='authors']/a/@data-event-content").extract_first()
        main_price = response.xpath("//span[@class='buying-priceold-val-number']/text()").extract_first()
        discount_price = response.xpath("//span[@class='buying-pricenew-val-number']/text()").extract_first()
        rating = response.xpath("//div[@id='rate']/text()").extract_first()

        yield BookparserItem(item_name=name,
                             item_author=author,
                             item_main_price=main_price,
                             item_discount_price=discount_price,
                             item_rating=rating,
                             item_link=link)

        print(name, author, main_price, discount_price, rating, link)

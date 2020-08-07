import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem

class Book24ruSpider(scrapy.Spider):
    name = 'book24ru'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=%D0%B1%D1%83%D0%BB%D0%B3%D0%B0%D0%BA%D0%BE%D0%B2']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains(@class,'catalog-pagination__item _text')]/@href").extract_first()
        book_title_links = response.xpath("//a[contains(@class, 'book__title-link')]/@href").extract()
        for link in book_title_links:
            yield response.follow(link, callback=self.book_parse)

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response:HtmlResponse):
        link = response.url
        name = response.xpath("//h1/text()").extract_first()
        author = response.xpath("//span[contains(@class, 'item-tab')]/a/text()").extract_first()
        main_price = response.xpath("//div[@class='item-actions__price-old']/text()").extract_first()
        discount_price = response.xpath("//div[@class='item-actions__price']/b/text()").extract_first()
        rating = response.xpath("//span[@class='rating__rate-value']/text()").extract_first()

        yield BookparserItem(item_name=name,
                             item_author=author,
                             item_main_price=main_price,
                             item_discount_price=discount_price,
                             item_rating=rating,
                             item_link=link)

        print(name, author, main_price, discount_price, rating, link)

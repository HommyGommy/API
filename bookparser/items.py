# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookparserItem(scrapy.Item):
    _id = scrapy.Field()
    item_name = scrapy.Field()
    item_author = scrapy.Field()
    item_main_price = scrapy.Field()
    item_discount_price = scrapy.Field()
    item_rating = scrapy.Field()
    item_link = scrapy.Field()
    pass

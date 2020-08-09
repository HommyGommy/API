# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

def process_photos(value):
    if value[:2] == '//':
        return f'http:{value}'
    return value

class LeroyItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(process_photos))
    price = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    chars = scrapy.Field()
    keys_chars = scrapy.Field(input_processor=MapCompose())
    values_chars = scrapy.Field(input_processor=MapCompose(lambda x: x.strip()))

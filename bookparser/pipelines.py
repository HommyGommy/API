# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class BookparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.books

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        link = item['item_link']
        book_title = item['item_name']
        author = item['item_author']
        main_price = item['item_main_price']
        discount_price = item['item_discount_price']
        rating = item['item_rating']

        collection.insert_one(item)
        for i in self.mongo_base:
            collection.update_one({'link': i['link']}, {'$set': i}, upsert=True)
        return item

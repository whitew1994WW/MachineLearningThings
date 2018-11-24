# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
import re

class MongoPipeline(object):
    collection_name = 'scrapy_items'

    def __init__(self):
        print("Starting mongodb")
        print("testing mongo client")

        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        item = extract_info(item)

        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            log.msg("Question added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item

    def extract_info(self, item):
        # Create a new object to reieve the actual values
        item_extracted = {}
        item_extracted['ingredients'] = extract_ingredients(item)
        item_extracted['method'] = extract_method(item)
        item_extracted['nutrition'] = extract_nutrition(item)
        item_extracted['title'] = extract_title(item)
        item_extracted['rating'] = extract_rating(item)
        item_extracted['prep_time'] = extract_prep_time(item)
        item_extracted['cook_time'] = extract_cook_time(item)
        item_extracted['skill'] = extract_skill(item)
        item_extracted['servings'] = extract_servings(item)
        return item_extracted

    def extract_ingredients(self, item):

        return ingredients

    def extract_method(self, item):

        return method

    def extract_nutrition(self, item):

        return nutrition

    def extract_title(self, item):

        return title

    def extract_rating(self, item):

        return rating

    def extract_prep_time(self, item):

        return prep_time

    def extract_cook_time(self, item):

        return cook_time

    def extract_skill(self, item):

        return skill

    def extract_servings(self, item):

        return servings
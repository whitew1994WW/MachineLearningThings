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
import HTMLParser
from HTMLParser2 import strip_tags

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

        new_item = self.extract_info(item)

        valid = True
        for data in new_item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(new_item)
            log.msg("Question added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item

    def extract_info(self, item):
        # Create a new object to reieve the actual values
        item_extracted = {}
        item_extracted['ingredients'] = self.extract_ingredients(item['ingredients'])
        item_extracted['method'] = self.extract_method(item['method'])
        item_extracted['nut'] = self.extract_nutrition(item['nutrition'])
        item_extracted['title'] = self.extract_title(item['title'])
        item_extracted['rating'] = self.extract_rating(item['rating'])
        item_extracted['prep_time'] = self.extract_prep_time(item['prep_time'])
        item_extracted['cook_time'] = self.extract_cook_time(item['cook_time'])
        item_extracted['skill'] = self.extract_skill(item['skill'])
        item_extracted['servings'] = self.extract_servings(item['servings'])
        return item_extracted

    def find_reg(self, regex, text):
        matches = re.finditer(regex, text, re.MULTILINE)
        groups = [match.group(1) for match in matches]
        if len(groups) == 0:
            groups = [None]
        return groups

    def extract_ingredients(self, text_list):
        if text_list == None:
            return None
        ingredients = []
        for text in text_list:
            ingredients.append(self.find_reg(r'content=\"([^\"]*)\">', text)[0])
        return ingredients

    def extract_method(self, text_list):
        if text_list == None:
            return None
        method = []
        for text in text_list:
            method.append(strip_tags(self.find_reg(r'<li class=\"method__item\" itemprop=\"recipeInstructions\">(.+?)</li>', text)[0]))
        return method

    def extract_nutrition(self, text_list):
        if text_list == None:
            return None
        nutrition = {}
        # Here using a list to make sure that if there is no nutritional information then the code still runs
        for text in text_list:
            nutrition['cal'] = self.find_reg(r'\"calories\">([\d\.]*)<', text)[0]
            nutrition['fat'] = self.find_reg(r'\"fatContent\">([\d\.]*)g<', text)[0]
            nutrition['sat'] = self.find_reg(r'\"saturatedFatContent\">([\d\.]*)g<', text)[0]
            nutrition['carbs'] = self.find_reg(r'\"carbohydrateContent\">([\d\.]*)g<', text)[0]
            nutrition['sugar'] = self.find_reg(r'\"sugarContent\">([\d\.]*)g<', text)[0]
            nutrition['fiber'] = self.find_reg(r'\"fiberContent\">([\d\.]*)g<', text)[0]
            nutrition['protein'] = self.find_reg(r'\"proteinContent\">([\d\.]*)g<', text)[0]
            nutrition['salt'] = self.find_reg(r'\"sodiumContent\">([\d\.]*)g<', text)[0]

        return nutrition

    def extract_title(self, text_list):
        if text_list == None:
            return None
        title = None
        for text in text_list:
            title = self.find_reg(r">(.*)<", text)[0]
            # Replace ampersands and remove semi-colons
            title = HTMLParser.HTMLParser().unescape(title)
        return title

    def extract_rating(self, text_list):
        if text_list == None:
            return None
        rating = None
        for text in text_list:
            rating = self.find_reg(r"\"ratingValue\" content=\"([\d\.]*)", text)[0]

        return rating

    def extract_prep_time(self, text_list):
        if text_list == None:
            return None
        prep_time = None
        for text in text_list:
            prep_time = self.find_reg(r'class=\"mins\">(\d*) mins', text)[0]
        return prep_time

    def extract_cook_time(self, text_list):
        if text_list == None:
            return None
        cook_time = None
        for text in text_list:
            cook_time = self.find_reg(r'class=\"mins\">(\d*) mins', text)[0]
        return cook_time

    def extract_skill(self, text_list):
        if text_list == None:
            return None
        skill = None
        for text in text_list:
            skill = self.find_reg(r'class=\"recipe-details__text\"> ([\w_\-\s]*) </span>', text)[0]
        return skill

    def extract_servings(self, text_list):
        if text_list == None:
            return None
        servings = None
        for text in text_list:
            servings = self.find_reg(r'itemprop=\"recipeYield\"> Serves (\d*) </', text)[0]
        return servings
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RecipeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ingredients = scrapy.Field()
    method = scrapy.Field()
    nutrition = scrapy.Field()
    title = scrapy.Field()
    rating = scrapy.Field()
    prep_time = scrapy.Field()
    cook_time = scrapy.Field()
    skill = scrapy.Field()
    servings = scrapy.Field()

    pass

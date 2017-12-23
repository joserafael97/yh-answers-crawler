# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QuestionItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    following = scrapy.Field()
    answers_number = scrapy.Field()
    last_answers = scrapy.Field()


class YhanswersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

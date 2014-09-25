# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProfileItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    photo = scrapy.Field()

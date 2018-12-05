# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class SpecialItem(scrapy.Item):
    special_id = scrapy.Field()
    special = scrapy.Field()


class Jianshuv2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    publish_time = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    words_count = scrapy.Field()
    page_url = scrapy.Field()
    user_profile = scrapy.Field()
    comments_count = scrapy.Field()
    likes_count = scrapy.Field()
    views_count = scrapy.Field()
    special_id = scrapy.Field()
    special = scrapy.Field()

item = SpecialItem(special_id=12312,special='')
if not item['special']:
    print('123123')
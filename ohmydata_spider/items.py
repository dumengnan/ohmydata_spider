#!/usr/bin/python
# -*- coding:utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html


from scrapy.item import Item, Field


class TutorialItem(Item):
    # define the fields for your item here like:
    # name = Field()
    proxy_url = Field()
    proxy_type = Field()
    proxy_locate = Field()


class DataTreasureItem(Item):
    book_name = Field()
    book_description = Field()



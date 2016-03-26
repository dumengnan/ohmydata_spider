#!/usr/bin/python
# -*- coding:utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from scrapy.selector import Selector


__author__ = 'mee'


class FreeweiboSpider(RedisSpider):

    name = "freeweibo"

    start_urls = (
        'https://freeweibo.com',
    )

    proxy = 'GFW'

    def parse(self, response):
        response_sel = Selector(response)


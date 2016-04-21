#!/usr/bin/python
# -*- coding:utf-8 -*-

__author__ = 'mee'
from scrapy_redis.spiders import RedisSpider
from scrapy.selector import Selector
from scrapy.http import Request
from ohmydata_spider.items import TmallCommentItem
import re
import ohmydata_spider.pipelines


class TestSpider(RedisSpider):
    name = "SpiderTest"

    start_urls = (
        "http://weibo.cn/pub/",
    )
    proxy = ''

    def parse(self, response):
        response_sel = Selector(response)

        hot_weibo = response_sel.xpath(u'//a[contains(@href, "http")]/@href')

        print hot_weibo.extract()


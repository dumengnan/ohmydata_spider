#!/usr/bin/python
# -*- coding:utf-8 -*-

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from ohmydata_spider.spiders.myspider import MySpider
from scrapy.utils.log import configure_logging

configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
spider = MySpider()
runner = CrawlerRunner()

d = runner.crawl(spider)
d.addBoth(lambda _:reactor.stop())
reactor.run()

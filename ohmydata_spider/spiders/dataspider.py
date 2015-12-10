#!/usr/bin/python
# -*- coding:utf-8 -*-

__author__ = 'mee'
from scrapy_redis.spiders import RedisSpider
from scrapy.selector import Selector
from ohmydata_spider.util.select_result import list_first_item,clean_url
from scrapy.http import Request
from ohmydata_spider.items import DataTreasureItem

class DataSpider(RedisSpider):
    name = "ohmygourd"
    start_urls = (
        'http://www.woaidu.org/sitemap_1.html',
    )

    def parse(self, response):
        response_sel = Selector(response)

        next_link = list_first_item(response_sel.xpath(u'//div[@class="k2"]/div/a[text()="下一页"]/@href').extract())

        if next_link:
            next_link = clean_url(response.url,next_link, response.encoding)
            yield Request(url=next_link,callback=self.parse)

        for detail_link in response_sel.xpath(u'//div[contains(@class,"sousuolist")]/a/@href').extract():
            if detail_link:
                detail_link = clean_url(response.url,detail_link,response.encoding)
                yield Request(url=detail_link, callback=self.parse_detail)


    def parse_detail(self,response):
        data_item = DataTreasureItem()

        response_selector = Selector(response)
        data_item['book_name'] = list_first_item(response_selector.xpath('//div[@class="zizida"][1]/text()').extract())
        data_item['book_description'] = list_first_item(response_selector.xpath('//div[@class="lili"][1]/text()').extract()).strip()

        yield data_item






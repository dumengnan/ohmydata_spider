#!/usr/bin/python
# -*- coding:utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.selector import Selector
from ohmydata_spider.util.select_result import list_first_item,clean_url
from scrapy.http import Request
from ohmydata_spider.items import TutorialItem

class MySpider(RedisSpider):
    name = 'myspider'
    start_urls = (
       'http://www.kjson.com/proxy/index/1',
    )
    proxy_porturl = {
        "/welcome/port?p=0632efa6a661399532d58b3067c2fc58":80,
        "/welcome/port?p=b276cf41e307d05f0ae916033d7fd2e3":1080,
        "/welcome/port?p=924f319b7b5e8e6324dd8635a019b262":8080,
        "/welcome/port?p=cea606afd9449152247d850abc1ec101":8088,
        "/welcome/port?p=31c21daeb91cb8e885927c1f7e23a9ac":8888,
        "/welcome/port?p=537ebe832aaaa219040f0719ebcc88c2":8118,
        "/welcome/port?p=1f20fab73dffd2f111f54f6e4178b009":8008,
        "/welcome/port?p=df05876b3d66ef4b4520cd3fd1281e04":3128,
        "/welcome/port?p=06d8946406bf2bc2015454d257016c84":8123,
        "/welcome/port?p=b8c44ce6567439c853b985e6ae720205":55336
    }

    def parse(self, response):
        response_sel = Selector(response)

        next_link =list_first_item(response_sel.xpath(u'//div[@class="page"]/a[text()="下一页"]/@href').extract())

        if next_link:
            next_link = clean_url(response.url, next_link, response.encoding)
            yield Request(url=next_link,callback=self.parse)

        for item in self.parse_detail(response): # 必须使用for循环来调用parse_detail函数,否则只能解析第一个界面
            yield item


    def parse_detail(self,response):

        response_sel = Selector(response)
        table_bodys = response_sel.xpath('//*[@id="dataTables-example"]/tbody/tr')

        for table_body in table_bodys:
            proxy_item = TutorialItem()
            port_url = str(list_first_item(table_body.xpath('./td[2]/img/@src').extract())).split('&')[0]

            if port_url in self.proxy_porturl:
                proxy_item['proxy_port'] = self.proxy_porturl[port_url]
                proxy_item['proxy_ip'] = list_first_item(table_body.xpath('./td[1]/text()').extract())
                proxy_item['proxy_type'] = list_first_item(table_body.xpath('./td[3]/text()').extract())
                proxy_item['proxy_locate'] = list_first_item(table_body.xpath('./td[7]/text()').extract())
            else:
                continue

            yield proxy_item








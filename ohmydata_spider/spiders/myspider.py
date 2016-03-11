#!/usr/bin/python
# -*- coding:utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.selector import Selector
from ohmydata_spider.util.select_result import list_first_item,clean_url
from scrapy.http import Request
from ohmydata_spider.items import TutorialItem
import ohmydata_spider.pipelines


class MySpider(RedisSpider):
    name = 'myspider'
    start_urls = ('http://www.kjson.com/proxy/index/1',)

    pipeline = set([
        ohmydata_spider.pipelines.MongoDBPipeline,
    ])

    proxy_porturl = {
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAIAAAAC64paAAAB1UlEQVQ4jdWTzcspYRjGH9OxGdLIRhTNQhYWSKmxGxtJxrBQNvwDSlnxH8hCNkgWsrSwEU1Z2dhbKJqGRvlI81FY6NH0dBbzHm9HZ+Ws3mv13Pdz/+q+rroNEELwqbCPyZ8L/3q9eJ5vtVqr1Qoh5Pf7y+Wyy+UCACCE2u32ZDJBCDEMUywWv2kIIYRQVVWaphuNhqqql8ulWq2mUin9q9frsSy73+83m000Gh0Oh/CPvtY+Ho+32y2Xy5lMJoIg4vH4+XxGCAEARqNRPp+32+0kSTIMw3Hcu2eSJB0OR7fb1TTter0OBoNYLIZhmCRJkiT5fD59zOv1CoLwDhuNxk6nI4piKpViWdbj8VQqFQCALMsAAKvVqo8RBPF4PDRNe097sVhst9t0Oh2JRDiOWy6XeloAAAz7GjMYDH/FrVuXZZmiqOl0qpf1ej2ZTEIIBUEIhUK73U7vz2YzmqbfAzscDs/nMxgM6iVFUafTCSHkdDpxHF+v13p/s9m8/H+v7Xa7zWZzv9+/3++KogyHw0AggGEYhmGJRGIwGCiKIorieDzOZrMv2PC6qtVq1Ww2eZ7HcTwcDpdKJZvNpvuq1Wrz+dxisRQKhUwm8w/4A/3Qq/ov+Dc2O/z/LmddcAAAAABJRU5ErkJggg==":'80',
    }

    def parse(self, response):
        response_sel = Selector(response)

        next_link = list_first_item(response_sel.xpath(u'//div[@class="page"]/a[text()="下一页"]/@href').extract())

        if next_link:
            next_link = clean_url(response.url, next_link, response.encoding)
            yield Request(url=next_link, callback=self.parse)

        print next_link
        # 必须使用for循环来调用parse_detail函数,否则只能解析第一个界面
        for item in self.parse_detail(response):
            yield item

    def parse_detail(self, response):
        response_sel = Selector(response)

        table_bodys = response_sel.xpath('//*[@id="dataTables-example"]/tbody/tr')

        for table_body in table_bodys:
            proxy_item = TutorialItem()
            port_url = str(list_first_item(table_body.xpath('./td[2]/img/@src').extract())).split('&')[0]

            if port_url in self.proxy_porturl:
                proxy_item['proxy_url'] = list_first_item(table_body.xpath('./td[1]/text()').extract()) + ':' + self.proxy_porturl[port_url]
                proxy_item['proxy_type'] = list_first_item(table_body.xpath('./td[3]/text()').extract())
                proxy_item['proxy_locate'] = list_first_item(table_body.xpath('./td[7]/text()').extract())
            else:
                continue
            yield proxy_item








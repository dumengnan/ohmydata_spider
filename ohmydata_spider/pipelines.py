#!/usr/bin/python
# -*- coding:utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from scrapy.conf import settings
from scrapy import log
import pymongo

class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['SingleMONGODB_SERVER'],
            settings['SingleMONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        if spider.name is not "myspider": #判断是否是对应的爬虫，如果不是返回item,保证只有相应的pipeline来处理对应的item
            return item

        print "proxy ip is :  " + str(item['proxy_ip'])
        print 'proxy port is : ' + str(item['proxy_port'])
        print 'proxy type is : ' + item['proxy_type']
        print 'proxy locate is :' + item['proxy_locate']

        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            log.msg("proxy ip added to MonogoDB database",
                    level=log.DEBUG,spider=spider)

        return item

class DataTreasurePipeline(object):

    def process_item(self,item,spider):
        if spider.name not in ['ohmygourd']:
            return item

        print 'book name is :' + item['book_name']
        print 'book description is ' + item['book_description']

        return item


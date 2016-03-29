#!/usr/bin/python
# -*- coding:utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from scrapy.conf import settings
import logging
import pymongo
import functools


def check_spider_pipeline(process_item_method):

    @functools.wraps(process_item_method)
    def wrapper(self, item, spider):

        # message for debugging
        msg = '%%s %s pipeline step'%(self.__class__.__name__,)
        logger = logging.getLogger(spider.name)
        if self.__class__ in spider.pipeline:
            logger.info(msg % 'executing')
            return process_item_method(self, item, spider)
        else:
            return item

    return wrapper


class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['SingleMONGODB_SERVER'],
            settings['SingleMONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    @check_spider_pipeline
    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            self.logger.info("proxy ip added to MonogoDB database")

        return item


class DataTreasurePipeline(object):

    @check_spider_pipeline
    def process_item(self, item, spider):
        print 'book name is :' + item['book_name']
        print 'book description is ' + item['book_description']

        return item


class JdBookPipeline(object):

    @check_spider_pipeline
    def process_item(self, item, spider):
        return item


class TmallCommentPipeline(object):

    @check_spider_pipeline
    def process_item(self, item, spider):
        return item


class WeiboPipeline(object):

    @check_spider_pipeline
    def process_item(self, item, spider):
        return item

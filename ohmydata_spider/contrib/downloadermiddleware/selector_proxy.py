#!/usr/bin/python
# -*- coding:utf-8 -*-

__author__ = 'mee'

import base64
import random
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
import pymongo
import logging


class SelectorProxyMiddlerware(HttpProxyMiddleware):  # 中间件继承时一定要有__init__方法，否则不会被执行

    # 实例化类时进行数据库连接
    def __init__(self):
        SingleMONGODB_SERVER = "localhost"
        SingleMONGODB_PORT = 27017
        MONGODB_DB = "proxyip_data"
        MONGODB_COLLECTION = "proxyip_collection"

        try:
            connection = pymongo.MongoClient(
                SingleMONGODB_SERVER,
                SingleMONGODB_PORT
            )

            db = connection[MONGODB_DB]
            self.collection = db[MONGODB_COLLECTION]
        except Exception, e:
            logging.warning("connection mongodb error %s", e.message)

    def process_request(self, request, spider):

        proxy = self.getproxy_ip(spider.proxy)

        if proxy is not None:
            logger = logging.getLogger(spider.name)
            logger.info("Select the proxy : %s" % (proxy['proxy_url']))
            if proxy['user_pass'] is not None:
                request.meta['proxy'] = proxy['proxy_url']
                encoded_user_pass = base64.encodestring(proxy['user_pass']).strip()
                request.headers['Proxy-Authorization'] = 'Basic' + encoded_user_pass
            else:
                request.meta['proxy'] = proxy['proxy_url']

    # 随机选取一个代理
    def getproxy_ip(self, proxy_type):
        try:
            if proxy_type == 'http':
                proj = self.collection.find({"proxy_type": "HTTP"}, {"proxy_url": 1})
                proj.skip(random.randint(0, proj.count()))
                proxy_info = proj.limit(-1).next()
                proxy_dict = {'proxy_url': "http://%s"%(proxy_info['proxy_url']), "user_pass": None}

            elif proxy_type == 'https':
                proj = self.collection.find({"proxy_type": "HTTPS"}, {"proxy_url": 1})
                proj.skip(random.randint(0, proj.count()))
                proxy_info = proj.limit(-1).next()
                proxy_dict = {'proxy_url': "https://%s"%(proxy_info['proxy_url']), "user_pass": None}

            elif proxy_type == 'GFW':
                proxy_dict = {'proxy_url': "http://127.0.0.1:8118", "user_pass": None}

            return proxy_dict
        except Exception, e:
            self.logger.warning("Get proxy Exception from mongodb warn info: %s", e.message)
            return None


if __name__ == '__main__':
    test_proxy = SelectorProxyMiddlerware()
    # test_proxy.getproxy_ip()
    # test_proxy.process_request(request="",spider="")

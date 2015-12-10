#!/usr/bin/python
# -*- coding:utf-8 -*-

__author__ = 'mee'

import base64
import random
from scrapy.contrib.downloadermiddleware.httpproxy import HttpProxyMiddleware
import pymongo


class SelectorProxyMiddlerware(HttpProxyMiddleware):  # 中间件继承时一定要有__init__方法，否则不会被执行

    def __init__(self):
        pass

    def process_request(self, request, spider):
        print 'spider name is !!!!!!!!!' + spider.name
        if spider.name is not 'ohmygourd':  # 不需要代理的爬虫直接不使用该组件
            try:
                return HttpProxyMiddleware.process_request(self,request,spider)
            except AttributeError:
                return super(SelectorProxyMiddlerware, self).process_request(request, spider)

        proxy = self.getproxy_ip()

        if proxy is not None:
            if proxy['user_pass'] is not None:
                request.meta['proxy'] = "http://%s" % (proxy['ip_port'])
                encoded_user_pass = base64.encodestring(proxy['user_pass']).strip()
                request.headers['Proxy-Authorization'] = 'Basic' + encoded_user_pass

            else:
                request.meta['proxy'] = "http://%s" % (proxy['ip_port'])

    def getproxy_ip(self):
        proxy_content = {}
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
            collection = db[MONGODB_COLLECTION]

            proj = collection.find({"proxy_type": "HTTP"}, {"proxy_ip": 1, "proxy_port": 1})

            proj.skip(random.randint(0, proj.count()))

            proxy_info = proj.limit(-1).next()

            print proxy_info

            proxy_dict = {"ip_port": proxy_info['proxy_ip'] + ":" + str(proxy_info['proxy_port']), "user_pass": None}

            return proxy_dict
        except Exception, e:
            print 'get proxy find exception ' + e.message
            return None


if __name__ == '__main__':
    test_proxy = SelectorProxyMiddlerware()
    # test_proxy.getproxy_ip()
    # test_proxy.process_request(request="",spider="")

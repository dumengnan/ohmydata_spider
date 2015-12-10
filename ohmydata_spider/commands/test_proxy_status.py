#!/usr/bin/python
# -*- coding:utf-8 -*-

__author__ = 'mee'

import urllib2
import pymongo

proxy_flag = 1

class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        global proxy_flag
        proxy_flag = 0
        return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
    http_error_301 = http_error_303 = http_error_307 = http_error_302

def Test_ProxyStatu(proxy_ip):  #通过使用代理ip打开一个url,通过返回码判断代理是否可用
    try:
        proxy = urllib2.ProxyHandler({'http':proxy_ip['ip_port']})

        cookieprocessor = urllib2.HTTPCookieProcessor()

        opener = urllib2.build_opener(MyHTTPRedirectHandler,cookieprocessor)
        opener.add_handler(proxy)

        urllib2.install_opener(opener)

        response = urllib2.urlopen('http://www.woaidu.org/sitemap_1.html',timeout=5)
        print response.read()
        return response.getcode()

    except Exception,e:
        print 'except reason ' + str(e.args)

def main():
    SingleMONGODB_SERVER="localhost"
    SingleMONGODB_PORT=27017
    MONGODB_DB="proxyip_data"
    MONGODB_COLLECTION="proxyip_collection"

    try:
        connection =  pymongo.MongoClient(
            SingleMONGODB_SERVER,
            SingleMONGODB_PORT
        )

        db = connection[MONGODB_DB]
        collection = db[MONGODB_COLLECTION]

        for proxy in collection.find({"proxy_type":"HTTP"},{"proxy_ip":1,"proxy_port":1}):
            proxy_dict = {}
            global proxy_flag
            proxy_flag = 1
            proxy_dict['ip_port'] = proxy['proxy_ip'] + ":" + str(proxy['proxy_port'])
            if Test_ProxyStatu(proxy_dict) == 200 and proxy_flag == 1:   #按顺序检测所有的代理ip是否可用，如果不可用，将其从数据库中移除
                print proxy_dict
            else:
                collection.remove({'proxy_ip':proxy['proxy_ip']})

    except Exception,e:
        print 'exception error ' + e.message

if __name__ == '__main__':
    #main()
    print 'return code is ' + str(Test_ProxyStatu({'ip_port':"http://111.13.2.143:80",'user_pass':None}))

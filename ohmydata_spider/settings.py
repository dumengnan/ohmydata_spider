#!/usr/bin/python
# -*- coding:utf-8 -*-

# Scrapy settings for ohmydata_spider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#


BOT_NAME = 'ohmydata_spider'
BOT_VERSION = '0.1'

SPIDER_MODULES = ['ohmydata_spider.spiders']
NEWSPIDER_MODULE = 'ohmydata_spider.spiders'
ITEM_PIPELINES = {
    'ohmydata_spider.pipelines.DataTreasurePipeline',
    'ohmydata_spider.pipelines.MongoDBPipeline',
}

#设置等待时间缓解服务器压力,并能够隐藏自己
DOWNLOAD_DELAY = 2

RANDOMIZE_DOWNLOAD_DELAY = True

#关闭默认的s3下载处理器
DOWNLOAD_HANDLERS = {'s3':None,}
#下载中间件设置，下载中间件用于修改全局scrapy　request和response．
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware':110,
    'ohmydata_spider.contrib.downloadermiddleware.selector_proxy.SelectorProxyMiddlerware':100,
    'scrapy.contrib.downloadermiddlewares.useragent.UserAgentMiddleware':None,
    'ohmydata_spider.contrib.downloadermiddleware.rotate_useragent.RotateUserAgentMiddleware':400,#将中间件中的user_agent修改为自己实现的部分
}
USER_AGENT = ''

#爬虫状态信息
#STATS_CLASS = 'ohmydata_spider.scrapy_graphite.graphite.RedisGraphiteStatsCollector'

#graphite 设置
#GRAPHITE_HOST = 'localhost'
#GRAPHITE_PORT = 2003
#GRAPHITE_IGNOREKEYS = []


COOKIES_ENABLED=False #禁用cookie

#redis调度器相关设置部分
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'

SCHEDULER_PERSIST = True

SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'

SCHEDULER_IDLE_BEFORE_CLOSE = 10


#数据存储部分设置
SingleMONGODB_SERVER="localhost"
SingleMONGODB_PORT=27017
MONGODB_DB="proxyip_data"
MONGODB_COLLECTION="proxyip_collection"

ShardMONGODB_SERVER="localhost"
ShardMONGODB_PORT=27017
ShardMONGODB_DB="proxyip_mongo"
GridFs_Collection="proxyip_table"


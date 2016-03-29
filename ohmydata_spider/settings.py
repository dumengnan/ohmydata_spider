#!/usr/bin/python
# -*- coding:utf-8 -*-

# Scrapy settings for ohmydata_spider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

SPIDER_MODULES = ['ohmydata_spider.spiders']
NEWSPIDER_MODULE = 'ohmydata_spider.spiders'
ITEM_PIPELINES = {
    'ohmydata_spider.pipelines.DataTreasurePipeline': 100,
    'ohmydata_spider.pipelines.MongoDBPipeline': 200,
    'ohmydata_spider.pipelines.JdBookPipeline': 300,
    'ohmydata_spider.pipelines.TmallCommentPipeline': 400,
}

# 设置等待时间缓解服务器压力,并能够隐藏自己
DOWNLOAD_DELAY = 2

RANDOMIZE_DOWNLOAD_DELAY = True

# 关闭默认的s3下载处理器
DOWNLOAD_HANDLERS = {'s3':None,}
# 下载中间件设置，下载中间件用于修改全局scrapy　request和response．
DOWNLOADER_MIDDLEWARES = {
    # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware':110,
    # 'ohmydata_spider.contrib.downloadermiddleware.selector_proxy.SelectorProxyMiddlerware':100,
    'scrapy.extensions.downloadermiddlewares.useragent.UserAgentMiddleware':None,
    'ohmydata_spider.contrib.downloadermiddleware.rotate_useragent.RotateUserAgentMiddleware':400,#将中间件中的user_agent修改为自己实现的部分
    'ohmydata_spider.contrib.downloadermiddleware.Cookie.CookiesMiddleware':401,
}
USER_AGENT = ''

# 爬虫状态信息
STATS_CLASS = 'ohmydata_spider.scrapy_graphite.graphite.RedisGraphiteStatsCollector'

# graphite 设置
GRAPHITE_HOST = 'localhost'
GRAPHITE_PORT = 2003
GRAPHITE_IGNOREKEYS = []

# 禁用cookie
# COOKIES_ENABLED = False
COOKIES_DEBUG=False

# redis调度器相关设置部分
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'

SCHEDULER_PERSIST = True

SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'

SCHEDULER_IDLE_BEFORE_CLOSE = 10

# 数据存储部分设置
SingleMONGODB_SERVER = "localhost"
SingleMONGODB_PORT = 27017
MONGODB_DB = "proxyip_data"
MONGODB_COLLECTION = "proxyip_collection"

ShardMONGODB_SERVER = "localhost"
ShardMONGODB_PORT = 27017
ShardMONGODB_DB = "proxyip_mongo"
GridFs_Collection = "proxyip_table"

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

# 数据序列化到文件
FEED_URI=u'WeiboInfo.csv'
FEED_FORMAT='CSV'
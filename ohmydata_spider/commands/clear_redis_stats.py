#!/usr/bin/python
# -*- coding:utf-8 -*-

__author__ = 'mee'

import redis

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
FILTER_KEY = 'myspider:dupefilter'
REQUEST_KEY = 'myspider:requests'
STATS_KEY = 'scrapy:stats'


def clear_stats():
    server = redis.Redis(REDIS_HOST,REDIS_PORT)
    server.delete(FILTER_KEY)
    server.delete(REQUEST_KEY)
    server.delete(STATS_KEY)


if __name__ == '__main__':
    clear_stats()

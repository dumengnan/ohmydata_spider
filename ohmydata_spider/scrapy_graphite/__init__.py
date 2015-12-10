#!/usr/bin/python
#-*-coding:utf-8-*-

__author__ = 'mee'
'''
    The module is from scrapy-graphite, The url https://github.com/noplay/scrapy-graphite
    You can install scrapy-graphite directly
    eg. pip install ScrapyGraphite

    Configure scrapy project:
    Set STATS_CLASS to scrapygraphite.GraphiteStatsCollector in your scrapy settings.py
    eg. STATS_CLASS = 'scrapygraphite.GraphiteStatsCollector'
        GRAPHITE_HOST= 'localhost'
        GRAPHITE_PORT = 2003

    Install grapite
    eg. pip install whisper(database)
        pip install carbon(monitor data, default port 2003)
        pip install graphite-web (web UI)


    In graphite you need to add in your storage-aggregation.conf
    [scrapy_min]
    pattern = ^scrapy\..*_min$
    xFilesFactor = 0.1
    aggregationMethod = min

    [scrapy_max]
    pattern = ^scrapy\..*_max$
    xFilesFactor = 0.1
    aggregationMethod = max

    [scrapy_sum]
    pattern = ^scrapy\..*_count$
    xFilesFactor = 0.1
    aggregationMethod = sum
'''
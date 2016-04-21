#!/usr/bin/python
# -*- coding:utf-8 -*-

import random
import logging
from ohmydata_spider.util.sinaCookie import cookies


__author__ = 'mee'


class CookiesMiddleware(object):

    def process_request(self, request, spider):
        cookie = random.choice(cookies)
        # logger = logging.getLogger(spider.name)
        # logger.info("Get the cookie: %s" % (cookie))
        request.cookies = cookie

#!/usr/bin/python
# -*- coding:utf-8 -*-

import urllib
import urlparse
from urlparse import urljoin
from w3lib.html import replace_entities


def clean_link(link_text):

    return link_text.strip("\t\r\n '\"")

# 返回第一个url地址
list_first_item = lambda x:x[0] if x else None 

# 将url地址组装返回,并移除空格标点　entites
clean_url = lambda base_url, u, response_encoding: urljoin(base_url, replace_entities(clean_link(u.decode(response_encoding))))


# 获取请求参数
def get_query(url, key):
    bits = list(urlparse.urlparse(url))
    query = urlparse.parse_qs(bits[4])

    return query[key][0]


# 设置请求参数
def set_query(url, **args):
    bits = list(urlparse.urlparse(url))
    query = urlparse.parse_qs(bits[4])

    for key in args:
        query[key] = args[key]

    bits[4] = urllib.urlencode(query, True)

    return urlparse.urlunparse(bits)

#!/usr/bin/python
# -*- coding:utf-8 -*-

import types
from urlparse import urlparse, urljoin
from w3lib.html import replace_entities


def clean_link(link_text):

    return link_text.strip("\t\r\n '\"")

#返回第一个url地址
list_first_item = lambda x:x[0] if x else None 

#将url地址组装返回,并移除空格标点　entites
clean_url = lambda base_url,u,response_encoding: urljoin(base_url,replace_entities(clean_link(u.decode(response_encoding))))




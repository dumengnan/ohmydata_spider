#!/usr/bin/python
# -*- coding:utf-8 -*-

import json
import base64
import requests
import logging

__author__ = 'mee'

'''
    Crawl Weibo Account
'''
WeiBoAccount = [
    {'user': 'ddcn00@mailnesia.com', 'psw': 'pp9999'},
    {'user': 'vhq30g@mailnesia.com', 'psw': 'pp9999'},
]


def getCookies(weibo):
    """
    function: get cookies
    :param weibo: weibo Account Info
    :return: cookies
    """
    cookies = []
    loginURL = r"https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)"
    for elem in weibo:
        account = elem['user']
        password = elem['psw']
        username = base64.b64encode(account.encode('utf-8')).decode('utf-8')

        postData = {
            "entry": "sso",
            "gateway": "1",
            "from": "null",
            "savestate": "30",
            "useticket": "0",
            "pagerefer": "",
            "vsnf": "1",
            "su": username,
            "service": "sso",
            "sp": password,
            "sr": "1440*900",
            "encoding": "UTF-8",
            "cdult": "3",
            "domain": "sina.com.cn",
            "prelt": "0",
            "returntype": "TEXT",
        }
        session = requests.Session()
        r = session.post(loginURL, data=postData)
        jsonStr = r.content.decode('gbk')
        info = json.loads(jsonStr)
        if info["retcode"] == "0":
            #logging.info("Cookie Account: %s"%(account))
            cookie = session.cookies.get_dict()
            cookies.append(cookie)
        else:
            logging.warn("Cookie get Failed : %s"%(info['reason']))

    return cookies

cookies = getCookies(WeiBoAccount)

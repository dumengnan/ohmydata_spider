#!/usr/bin/python
# -*- coding:utf-8 -*-
import codecs

f = open('TmallComment.json', 'r')
f2 = open('allTmallComment.json', 'w')
for text in f:
    try:
        f2.write(text.decode('unicode-escape').encode('utf-8'))
        print text.decode('unicode-escape').encode('utf-8')
    except Exception, e:
        print 'error'


#!/usr/bin/python
# -*- coding:utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html


from scrapy.item import Item, Field


class TutorialItem(Item):
    # define the fields for your item here like:
    # name = Field()
    proxy_url = Field()
    proxy_type = Field()
    proxy_locate = Field()


class DataTreasureItem(Item):
    book_name = Field()
    book_description = Field()


class JdBookItem(Item):
    number = Field()
    bookName = Field()
    author = Field()
    press = Field()
    bookId = Field()
    price = Field()
    preferentialPrice = Field()


class TmallCommentItem(Item):
    ItemName = Field()
    ItemType = Field()
    ItemSales = Field()
    ItemPrice = Field()
    itemId = Field()
    userNick = Field()
    rateDate = Field()
    rateContent = Field()


class WeiboInfoItem(Item):
    """
    weibo Account info
    """
    id = Field()
    NickName = Field()
    Gender = Field()
    Province = Field()
    City = Field()
    Signature = Field()
    Birthday = Field()
    Num_Tweets = Field()
    Num_Follows = Field()
    Num_Fans = Field()
    Sex_Orientation = Field()
    Marriage = Field()
    URL = Field()


class WeiboContentItem(Item):
    """
    weibo content info
    """
    id = Field()
    ID = Field()
    Content = Field()
    PubTime = Field()
    Co_oridinates = Field()  # location
    Tools = Field()  # publish tools eg.computer phone
    Like = Field()  # count of the like
    Comment = Field()  # count of the comment
    Transfer = Field()


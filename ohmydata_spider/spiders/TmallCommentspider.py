#!/usr/bin/python
# -*- coding:utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from ohmydata_spider.items import TmallCommentItem
from scrapy.selector import Selector
from scrapy.http import Request

from ohmydata_spider.util.select_result import get_query, set_query, clean_link
import ohmydata_spider.pipelines
import re, json
import logging


__author__ = 'mee'


class TmallCommentSpider(RedisSpider):

    name = "TmallComment"

    start_urls =(
        "https://suning.world.tmall.com/",
    )

    categoryUrl = "https://suning.world.tmall.com/category-1115569769.htm?search=y&catId=1115569769&pageNo=1"
    asyncUrl = "https://suning.world.tmall.com/i/asynSearch.htm?mid=null&wid=null&path=?&&search=y&catId=?&scid=?&pageNo=?"
    rateUrl = "https://rate.tmall.com/list_detail_rate.htm?itemId=522155891308&sellerId=2616970884&currentPage=1"

    pipeline = set([
        ohmydata_spider.pipelines.TmallCommentPipeline,
            ])

    proxy = 'GFW'

    def parse(self, response):
        response_sel = Selector(response)

        category = response_sel.xpath(u'//a[contains(@href,"category")]/@href').extract()

        all_category = set()
        for category_url in category:
            category_id = re.findall(r'category-(\d+).htm', category_url)
            if category_id:
                all_category.add(category_id[0])

        for category_id in all_category:
            result_url, result_count = re.subn(r'(\d+\d+)', category_id, self.categoryUrl)
            self.logger.info("category url : %s", result_url)
            yield Request(url=result_url, callback=self.parse_category)

    def parse_category(self, response):
        response_sel = Selector(response)
        data_widgetid = response_sel.xpath(u'//*[@class="J_TModule" and @data-title="搜索列表"]/@data-widgetid').extract()
        wid = data_widgetid[0]

        mid = 'w-' + wid + '-0'
        catId = get_query(response.url, 'catId')
        path = "/category"+catId + '.htm'
        pageNo = get_query(response.url, 'pageNo')

        page_url = set_query(self.asyncUrl, wid=wid, mid=mid, path=path, catId=catId, scid=catId,pageNo=pageNo)

        yield Request(url=page_url, callback=self.parse_nextpage)

    def parse_nextpage(self, response):
        response_sel = Selector(response)
        next_pageurl = response_sel.xpath(u'//a[contains(@class,"next")]/@href').extract()

        page_num = get_query(next_pageurl[0], 'pageNo')

        next_url = set_query(self.categoryUrl, pageNo=page_num)

        if next_url:
            yield Request(url=next_url, callback=self.parse_category)

        dl_bodys = response_sel.xpath(u'/html/body/div/div[3]')

        for dl_body in dl_bodys:
            item_lines = dl_body.xpath(u'./div/dl')
            for item_line in item_lines:
                data_id = item_line.xpath(u'./@data-id').extract()

                item_id = re.findall('(\d+)', data_id[0])

                comment_url = set_query(self.rateUrl,itemId=item_id[0])

                yield Request(url=comment_url, callback=self.parse_comment)

    def parse_comment(self, response):
        response_sel = Selector(response)

        allPageCount = re.findall('"lastPage\":(.+?)\,', response_sel.extract())[0]

        # 对每一页的评论进行解析
        i = 1
        while i < int(allPageCount):
            next_link = set_query(response.url, currentPage=i)

            i = i + 1
            yield Request(url=next_link, callback=self.parse_detail)

    def parse_detail(self, response):

        self.logger.info("parse url : %s", response.url)
        response_sel = Selector(response)
        commentJson = re.findall('\"rateList\":(\[.*?\])\,\"searchinfo\"', response_sel.extract())[0]

        for data in json.loads(commentJson):
            comment_item = TmallCommentItem()

            comment_item['itemId'] = get_query(response.url, 'itemId')
            comment_item['userNick'] = data['displayUserNick']
            comment_item['rateDate'] = data['rateDate']
            comment_item['rateContent'] = data['rateContent']

            yield comment_item

#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import json
from urlparse import urlparse
import urllib
import sys


from scrapy.selector import Selector
try:
    from scrapy.spider import Spider
except:
    from scrapy.spider import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.contrib.spiders import CrawlSpider, Rule, Spider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle
from scrapy.http import FormRequest, Request
from scrapy import log

from template.items import *
from template.settings import *
from misc.log import *
from misc.spider import CommonSpider


reload(sys)
sys.setdefaultencoding('utf-8')

class templateSpider(CommonSpider):
    name = "template"
    allowed_domains = ["template.com"]
    start_urls = [
        "http://www.template.com/",
    ]
    rules = [
        Rule(sle(allow=("/topsites/category;?[0-9]*/Top/World/Chinese_Simplified_CN/.*$")), callback='parse_11', follow=True),
    ]

    all_css_rules = {
        '.sslalone': {
            '__use': 'dump',
            '__list': True,
            'name': '.fl h4 a::text',
            'score': '.lp_fen .mr05.fb::text',
            'comment': '.lp_fen .fl.ml05 a[href*=dianping]::text',
            'price': '.fr h5 span::text',
            'sharp': '.pt08 .fl a::text',
            'address': '.fl.add a::text',
            'tel': '.pt04 .fr strong::text',
            'extra': '.fl.guanjianzi.hidden a::text',
        }
    }

    def parse_11(self, response):
        info('Parse depth 1 '+response.url)
        items = self.parse_with_rules(response, self.all_css_rules, templateItem)
        return items



    # def __init__(self, *args, **kwargs):
    #     super(templateSpider, self).__init__(*args, **kwargs)
    #     self.headers = HEADERS
    #     self.cookies = COOKIES



    # def start_requests(self):
    #     for i, url in enumerate(self.start_urls):
    #         yield FormRequest(url,
    #                           meta={'cookiejar': i},
    #                           headers=self.headers,
    #                           cookies=self.cookies,
    #                           callback=self.after_login
    #                           )



    # def start_requests(self):
    #     return [Request(
    #         "http://www.zhihu.com",
    #         callback=self.post_login
    #     )]



    # def post_login(self, response):
    #     log.msg(u"login  ing ........", level=log.INFO)
    #     xsrf = Selector(response).xpath('//input[@name="_xsrf"]/@value').extract()[0]
    #     #xsrf = Selector(response).css('input[name=_xsrf]::attr(value)').extract()[0]
    #     log.msg(u'xsrf: %s' % xsrf, level=log.INFO)
    #     return [FormRequest.from_response(
    #         response,
    #         formdata = {
    #         '_xsrf': xsrf,
    #         'email': '',
    #         'password': '',
    #         },
    #         callback = self.after_login
    #     )]


    # def start_requests(self):
    #     return [Request(
    #         "http://www.zhihu.com/login/email",
    #         headers=self.headers,
    #         # cookies=self.cookies,
    #         meta = {'cookiejar': 1},
    #         callback = self.post_login
    #     )]

    # def post_login(self, response):
    #     log.msg(u"login  ing ........", level=log.INFO)
    #     xsrf = Selector(response).css('input[name=_xsrf]::attr(value)').extract()[0]
    #     log.msg(u'xsrf: %s' % xsrf, level=log.INFO)
    #     return [FormRequest.from_response(response,
    #                                       meta = {'cookiejar': response.meta['cookiejar']},
    #                                       headers = self.headers,
    #                                       formdata = {
    #                                           '_xsrf': xsrf,
    #                                           'email': '',
    #                                           'password': '',
    #                                           'remember_me': 'false'
    #                                       },
    #                                       callback = self.after_login,
    #                                       dont_filter = True
    #                                       )]


    # def after_login(self, response):
    #     log.msg(u"--------response body------: %s" % response.body, level=log.INFO)
    #     # if "errcode" in response.body:
    #     #     log.msg(u"$$$$$$  Login Failed  $$$$$$", level=log.ERROR)
    #     #     return
    #     # else:
    #     #     log.msg(u'************ Login Success ************', level=log.INFO)
    #     # for url in self.start_urls:
    #     #     yield self.make_requests_from_url(url)
    #     log.msg("------------------------------------------------", level=log.INFO)
    #     return self.make_requests_from_url("http://www.zhihu.com/people/jia-yang-qing-74/followees")


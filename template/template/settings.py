# Scrapy settings for template project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import sys
import os
from os.path import dirname
path = dirname(dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(path)
from misc.log import *

BOT_NAME = 'template'

SPIDER_MODULES = ['template.spiders']
NEWSPIDER_MODULE = 'template.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'template (+http://www.yourdomain.com)'

DOWNLOADER_MIDDLEWARES = {
   # 'misc.middleware.CustomHttpProxyMiddleware': 400,
    'misc.middleware.CustomUserAgentMiddleware': 401,
}

ITEM_PIPELINES = {
    #'template.pipelines.JsonWithEncodingPipeline': 300,
    #'template.pipelines.RedisPipeline': 301,
    'template.pipelines.MyImagesPipeline': 1,
    'template.pipelines.MongoDBPipeline': 302,
}


IMAGES_STORE = '/path/to/your/dir'
# IMAGES_THUMBS = {
#     'small': (50, 50),
#     'big': (270, 270),
# }

# IMAGES_MIN_HEIGHT = 110
# IMAGES_MIN_WIDTH = 110


MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DATABASE = 'scrapy'
MONGODB_COLLECTION = 'zhihu_people'
MONGODB_UNIQ_KEY = '_id'

#add to test by wjr
# RETRY_TIMES = 10
# RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]
# COOKIES_ENABLED = False

#add to test by wjr
# CONCURRENT_REQUESTS = 100
# CONCURRENT_REQUESTS_PER_DOMAIN = 30


# COOKIES_ENABLED = True
# COOKIES_DEBUG = True

LOG_LEVEL = 'DEBUG'

DOWNLOAD_DELAY = 1



# HEADERS = {
#     "Accept": "*/*",
#     "Accept-Encoding": "gzip, deflate",
#     "Accept-Language": "zh-CN,zh;q=0.8",
#     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36",
#     "X-Requested-With": "XMLHttpRequest",
#     "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
#     "Connection": "keep-alive",
#     "Referer": "http://www.template.com/",
# }
#
#
# COOKIES = {
#     '__utma': r'51854390.46277521.1440378143.1440378143.1440380995.2',
#     '__utmb': r'51854390.6.10.1440380995',
#     '__utmc': r'51854390',
#     '__utmt': "1",
#     '__utmv': r'51854390.000--|3=entry_date=20150729=1',
#     '__utmz': r'51854390.1440380995.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
#     '_xsrf':  r'bffe87f0df0b7b01810b0079dfb454e3',
#     '_za': r'a301822c-ba2e-4047-aebf-1c0ba4d87967',
#     'cap_id': r'"NmQ2Njk0MGIzNjkyNDg2NTkwMTZiN2YwZDU4NDBiYTU=|1438139687|99826cfe1f5c083b344cdbab275f5e4b613cadf9"',
#     'q_c1': r'6f856d90e2494cacad4f50e9897634da|1438139687000|1438139687000',
#     'unlock_ticket': r'"QUJCSzRmOVdrUWdYQUFBQVlRSlZUVDJDMmxVX3ZneDNxVmJmVzVnZzRLcXJuzhubWxjQjVRPT0=|1440381749|0c9d4cb5da648cb7517f4a8e79cfc17309f3c1eb"',
#     'z_c0': r'"QUJCSzRmOVdrUWdYQUFBQVlRSlZUVFVJQWxaUWRoSlpBLXdNNUMwLXVOUjI4Z0NXNXZWMm1BPT0=|1440381749|55629de148b35d6e41f42956e7077930ba0d60f8"',
#     'client_id': r'"Mjg1MzI5NDQyNA==|1440377029|2b64ee0424d4c032a606c084962025303ab6a951"',
#     'token': r'"Mi4wMG9OSUdIREVBNzIyRDJmNDRlOWVhNTgwWnNBYjg=|1440377029|712dbe79d81dd24fec2e6d25887ab9c22c499ac0"',
#     'auth_type': r'"c2luYQ==|1440377029|0021b7c62120b200224845aab6c4ea436adf1ab4"',
#     'tc': r'AQAAAJWFhR/8nwkAgrpsccSLmXNKbwo+'
# }

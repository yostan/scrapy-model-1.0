# Scrapy settings for dmoz project
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

BOT_NAME = 'dmoz'

SPIDER_MODULES = ['dmoz.spiders']
NEWSPIDER_MODULE = 'dmoz.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'dmoz (+http://www.yourdomain.com)'

DOWNLOADER_MIDDLEWARES = {
   # 'misc.middleware.CustomHttpProxyMiddleware': 400,
    'misc.middleware.CustomUserAgentMiddleware': 401,
}

ITEM_PIPELINES = {
    'dmoz.pipelines.MongoDBPipeline': 300,
    #'dmoz.pipelines.RedisPipeline': 301,
}

MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DATABASE = 'scrapy'
MONGODB_COLLECTION = 'dmoz'
MONGODB_UNIQ_KEY = '_id'


LOG_LEVEL = 'INFO'

DOWNLOAD_DELAY = 1

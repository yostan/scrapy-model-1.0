# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import redis
import datetime

from scrapy import signals


import json
import codecs
from collections import OrderedDict
from scrapy import log
from scrapy.contrib.exporter import BaseItemExporter

from pymongo import errors
from pymongo.mongo_client import MongoClient
from pymongo.mongo_replica_set_client import MongoReplicaSetClient
from pymongo.read_preferences import ReadPreference

class JsonWithEncodingPipeline(object):

    def __init__(self):
        self.file = codecs.open('data_utf8.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()


class RedisPipeline(object):

    def __init__(self):
        self.r = redis.StrictRedis(host='localhost', port=6379)

    def process_item(self, item, spider):
        if not item['id']:
            print 'no id item!!'

        str_recorded_item = self.r.get(item['id'])
        final_item = None
        if str_recorded_item is None:
            final_item = item
        else:
            ritem = eval(self.r.get(item['id']))
            final_item = dict(item.items() + ritem.items())
        self.r.set(item['id'], final_item)

    def spider_closed(self, spider):
        return



def not_set(string):
    if string is None:
        return True
    elif string == "":
        return True
    return False



class MongoDBPipeline(BaseItemExporter):
    config = {
        'uri': 'mongodb://localhost:27017',
        'fsync': False,
        'write_concern': 0,
        'database': 'scrapy-mongodb',
        'collection': 'items',
        'replica_set': None,
        'unique_key': None,
        'buffer': None,
        'append_timestamp': False,
        'stop_on_duplicate': 0,
    }

    current_item = 0
    item_buffer = []
    duplicate_key_count = 0


    def configure(self):
        """ Configure the MongoDB connection """
        # Handle deprecated configuration
        if not not_set(self.settings['MONGODB_HOST']):
            log.msg(
                u'DeprecationWarning: MONGODB_HOST is deprecated',
                level=log.WARNING)
            mongodb_host = self.settings['MONGODB_HOST']

            if not not_set(self.settings['MONGODB_PORT']):
                log.msg(
                    u'DeprecationWarning: MONGODB_PORT is deprecated',
                    level=log.WARNING)
                self.config['uri'] = 'mongodb://{0}:{1:i}'.format(
                    mongodb_host,
                    self.settings['MONGODB_PORT'])
            else:
                self.config['uri'] = 'mongodb://{0}:27017'.format(mongodb_host)

        if not not_set(self.settings['MONGODB_REPLICA_SET']):
            if not not_set(self.settings['MONGODB_REPLICA_SET_HOSTS']):
                log.msg(
                    (
                        u'DeprecationWarning: '
                        u'MONGODB_REPLICA_SET_HOSTS is deprecated'
                    ),
                    level=log.WARNING)
                self.config['uri'] = 'mongodb://{0}'.format(
                    self.settings['MONGODB_REPLICA_SET_HOSTS'])

        # Set all regular options
        options = [
            ('uri', 'MONGODB_URI'),
            ('fsync', 'MONGODB_FSYNC'),
            ('write_concern', 'MONGODB_REPLICA_SET_W'),
            ('database', 'MONGODB_DATABASE'),
            ('collection', 'MONGODB_COLLECTION'),
            ('replica_set', 'MONGODB_REPLICA_SET'),
            ('unique_key', 'MONGODB_UNIQUE_KEY'),
            ('buffer', 'MONGODB_BUFFER_DATA'),
            ('append_timestamp', 'MONGODB_ADD_TIMESTAMP'),
            ('stop_on_duplicate', 'MONGODB_STOP_ON_DUPLICATE')
        ]

        for key, setting in options:
            if not not_set(self.settings[setting]):
                self.config[key] = self.settings[setting]

        if self.config['buffer'] and self.config['unique_key']:
            log.msg(
                (
                    u'IllegalConfig: Settings both MONGODB_BUFFER_DATA '
                    u'and MONGODB_UNIQUE_KEY is not supported'
                ),
                level=log.ERROR)
            raise SyntaxError(
                (
                    u'IllegalConfig: Settings both MONGODB_BUFFER_DATA '
                    u'and MONGODB_UNIQUE_KEY is not supported'
                ))


    def load_spider(self, spider):
        self.crawler = spider.crawler
        self.settings = spider.settings

        if not hasattr(spider, 'update_settings') and hasattr(spider, 'custom_settings'):
            self.settings.setdict(spider.custom_settings or {}, priority='project')


    def open_spider(self, spider):
        self.load_spider(spider)

        # Configure the connection
        self.configure()

        if self.config['replica_set'] is not None:
            connection = MongoReplicaSetClient(self.config['uri'],
                replicaSet=self.config['replica_set'],
                w=self.config['write_concern'],
                fsync=self.config['fsync'],
                read_preference=ReadPreference.PRIMARY_PREFERRED)
        else:
            # Connecting to a stand alone MongoDB
            connection = MongoClient(
                self.config['uri'],
                fsync=self.config['fsync'],
                read_preference=ReadPreference.PRIMARY)

        # Set up the collection
        database = connection[self.config['database']]
        self.collection = database[self.config['collection']]
        log.msg(u'Connected to MongoDB {0}, using "{1}/{2}"'.format(
            self.config['uri'],
            self.config['database'],
            self.config['collection']))

        # Ensure unique index
        if self.config['unique_key']:
            self.collection.ensure_index(self.config['unique_key'], unique=True)
            log.msg('uEnsuring index for key {0}'.format(
                self.config['unique_key']))


        # Get the duplicate on key option
        if self.config['stop_on_duplicate']:
            tmpValue = self.config['stop_on_duplicate']
            if tmpValue < 0:
                log.msg(
                    (
                        u'Negative values are not allowed for'
                        u' MONGODB_STOP_ON_DUPLICATE option.'
                    ),
                    level=log.ERROR
                )
                raise SyntaxError(
                    (
                        'Negative values are not allowed for'
                        ' MONGODB_STOP_ON_DUPLICATE option.'
                    )
                )
            self.stop_on_duplicate = self.config['stop_on_duplicate']
        else:
            self.stop_on_duplicate = 0




    def process_item(self, item, spider):
        """ Process the item and add it to MongoDB

        :type item: Item object
        :param item: The item to put into MongoDB
        :type spider: BaseSpider object
        :param spider: The spider running the queries
        :returns: Item object
        """

        item = dict(self._get_serialized_fields(item))
        if self.config['buffer']:
            self.current_item += 1
            if self.config['append_timestamp']:
                item['scrapy-mongodb'] = {'ts': datetime.datetime.utcnow()}
            self.item_buffer.append(item)
            if self.current_item == self.config['buffer']:
                self.current_item = 0
                return self.insert_item(self.item_buffer, spider)
            else:
                return item
        return self.insert_item(item, spider)


    def close_spider(self, spider):
        """ Method called when the spider is closed
        :type spider: BaseSpider object
        :param spider: The spider running the queries
        :returns: None
        """
        if self.item_buffer:
            self.insert_item(self.item_buffer, spider)


    def insert_item(self, item, spider):
        """ Process the item and add it to MongoDB

        :type item: (Item object) or [(Item object)]
        :param item: The item(s) to put into MongoDB
        :type spider: BaseSpider object
        :param spider: The spider running the queries
        :returns: Item object
        """
        if not isinstance(item, list):
            item = dict(item)
            if self.config['append_timestamp']:
                    item['scrapy-mongodb'] = {'ts': datetime.datetime.utcnow()}


        if self.config['unique_key'] is None:
            try:
                self.collection.insert(item, continue_on_error=True)
                log.msg(
                    u'Stored item(s) in MongoDB {0}/{1}'.format(
                        self.config['database'], self.config['collection']),
                    level=log.DEBUG,
                    spider=spider)
            except errors.DuplicateKeyError:
                log.msg(u'Duplicate key found', level=log.DEBUG)
                if (self.stop_on_duplicate > 0):
                    self.duplicate_key_count += 1
                    if (self.duplicate_key_count >= self.stop_on_duplicate):
                        self.crawler.engine.close_spider(
                            spider,
                            'Number of duplicate key insertion exceeded'
                        )
                pass
        else:
            key = {}
            if isinstance(self.config['unique_key'], list):
                for k in dict(self.config['unique_key']).keys():
                    key[k] = item[k]
            else:
                key[self.config['unique_key']] = item[self.config['unique_key']]

            self.collection.update(key, item, upsert=True)

            log.msg(
                u'Stored item(s) in MongoDB {0}/{1}'.format(
                    self.config['database'], self.config['collection']),
                level=log.DEBUG,
                spider=spider)
        return item



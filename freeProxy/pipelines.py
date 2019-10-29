# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.exceptions import NotConfigured


class MongoPipeline(object):
    
    #fresh_proxy保存新代理，会自动过期
    collection_name = 'fresh_proxy'
    
    #fresh_proxy中元素过期时间
    expire_time = 300

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        
    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('MONGOPIPELINE_ENABLED'):
            # if this isn't specified in settings, the pipeline will be completely disabled
            raise NotConfigured
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        col = self.db[self.collection_name]
        col.create_index("createtime",expireAfterSeconds=self.expire_time)


    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        result = self.db[self.collection_name].find_one({'_id': item['_id']})
        if result:
            self.db[self.collection_name].replace_one({'_id': item['_id']}, item)
        else:
            self.db[self.collection_name].insert_one(item)
        return item

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.exceptions import NotConfigured

#保存fresh代理
class MongoFreshProxyPipeline(object):
    
    #fresh_proxy保存新代理，会自动过期
    collection_name = 'fresh_proxy'
    
    #fresh_proxy中元素过期时间(s)
    expire_time = 3000

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        
    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('MONGO_FRESHPROXY_PIPELINE_ENABLED'):
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

#保存stable代理
class MongoStableProxyPipeline(object):
    
    #fresh_proxy保存新代理，会自动过期
    fresh_collection = 'fresh_proxy'
    stable_collection = 'stable_proxy'

    new_stable_proxies = []
    

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        
    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('MONGO_STABLEPROXY_PIPELINE_ENABLED'):
            # if this isn't specified in settings, the pipeline will be completely disabled
            raise NotConfigured
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        spider.pipeline = self

    def close_spider(self, spider):
        #替换全部stable_collection的内容
        self.db[self.stable_collection].delete_many({})
        #去重
        seen_ids = set()
        new_proxies = []
        for p in self.new_stable_proxies:
            if p['_id'] not in seen_ids:
                new_proxies.append(p)
            seen_ids.add(p['_id'])
        print(new_proxies)
        self.db[self.stable_collection].insert_many(new_proxies)
        self.client.close()
    
    #返回 fresh/stable中的全部代理地址
    def listProxy(self):
        stable_proxies = self.db[self.stable_collection].find({})
        fresh_proxies = self.db[self.fresh_collection].find({})
        proxies = []
        for sp in stable_proxies:
            proxies.append(sp)
        for fp in fresh_proxies:
            proxies.append(fp)
        return proxies     

    def process_item(self, item, spider):
        self.new_stable_proxies.append(item)    
        return item       

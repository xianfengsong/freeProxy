# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProxyItem(scrapy.Item):
    #自定义id,使用完整地址的值
    _id = scrapy.Field()
    
    #完整地址
    address = scrapy.Field()
    
    #地址提供者
    provider = scrapy.Field()
    
    #协议 http/https/socks5..
    protocol = scrapy.Field()
    
    #匿名程度 透明Transparent、匿名Anonymous、高匿Elite Proxy/High anonymity 
    anonymity =scrapy.Field()
    
    #所属国家
    country=scrapy.Field()

    #保存到mongo时间
    createtime=scrapy.Field()

from freeProxy.spiders import proxy_spider,check_spider
import scrapy
from scrapy.crawler import CrawlerProcess

process = CrawlerProcess()
process.crawl(proxy_spider)
process.crawl(check_spider)
process.start() # the script will block here until all crawling jobs are finished
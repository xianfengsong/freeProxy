import scrapy
from freeProxy.items import ProxyItem
import datetime

# 读取free-proxy-list.net的代理地址，通过访问google验证
# Returns:
# 代理信息 ProxyItem
class FreeProxyListSpider(scrapy.Spider):
    name = "free-proxy-list"
    start_urls = ['https://free-proxy-list.net/']

    custom_settings = {
        #超时2s
        'DOWNLOAD_TIMEOUT': 2
    }
    def parse(self,response):
        check_url = 'https://www.google.com'
        for tr in response.xpath('//*[@id="proxylisttable"]/tbody/tr'):
            
            proxyItem = ProxyItem()
            
            proxyItem['provider'] = 'free-proxy-list.net'
            proxyItem['country'] = tr.xpath('td[4]/text()').get()
            proxyItem['anonymity'] = tr.xpath('td[5]/text()').get()
            ip = tr.xpath('td[1]/text()').get()
            port = tr.xpath('td[2]/text()').get()

            if(tr.xpath('td[7]/text()').get() is not None):
                protocol = ''
                if (tr.xpath('td[7]/text()').get() == 'yes'):
                    protocol = 'https'
                elif(tr.xpath('td[7]/text()').get() == 'no'):
                    protocol = 'http'

                address = protocol+'://'+ip+':'+port
                proxyItem['address'] = address
                proxyItem['_id'] = address
                #构造检查请求
                yield scrapy.Request(check_url,callback=self.parseCheckResult,
                    meta={'proxy':address,'proxyItem':proxyItem},
                    dont_filter=True)
            else:    
                continue

    def parseCheckResult(self,response):
        print(response.request.meta)
        if response.xpath('//*[@id="hplogo"]') is not None:
            proxyItem = response.request.meta['proxyItem']
            proxyItem['createtime'] = datetime.datetime.utcnow()
            return proxyItem  
        
            
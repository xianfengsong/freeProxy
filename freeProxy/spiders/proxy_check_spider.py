import scrapy
import json

#读取proxy.jl文件中的代理地址，通过访问google验证
class ProxyCheckSpider(scrapy.Spider):
    name = "proxyCheck"
    #自定义配置
    custom_settings = {
        #超时1s
        'DOWNLOAD_TIMEOUT': 1
    }
    def start_requests(self):
        url = 'https://www.google.com'
        proxys = []
        with open('proxy.jl','r') as f:
            for line in f:
                proxys.append(json.loads(line)['proxy'])
        for proxy in proxys:
            yield scrapy.Request(url,callback=self.parse,meta={'proxy':proxy},dont_filter=True)

    def parse(self,response):
        print(response.request.meta)
        if response.xpath('//*[@id="hplogo"]') is not None:
            yield{
                'checkedProxy':response.request.meta['proxy']
            }
        
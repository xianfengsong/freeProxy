import scrapy

#读取mongodb fresh/stable_proxy集合中的代理，通过访问google验证
class CheckSpider(scrapy.Spider):
    name = "check"
    pipeline = None
    #自定义配置
    custom_settings = {
        #超时2s
        'DOWNLOAD_TIMEOUT': 2,
        'MONGO_FRESHPROXY_PIPELINE_ENABLED' :False,
    }


    def start_requests(self):
        url = 'https://www.google.com'
        
        proxies = self.pipeline.listProxy()
        
        for proxy in proxies:
           yield scrapy.Request(url,callback=self.parse,meta={'proxy':proxy['address'],'proxyItem':proxy}
           ,dont_filter=True)

    #返回proxyItemWrapper，标记代理是否可用
    def parse(self,response): 
        proxyItem = response.request.meta['proxyItem']
        if response.xpath('//*[@id="hplogo"]') is not None:
            return proxyItem
        else:
            return None
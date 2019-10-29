import scrapy
import requests
#使用代理的demo
class demoSpider(scrapy.Spider):
    name = "demo"
    pipeline = None
    #自定义配置
    custom_settings = {
        #超时2s
        'DOWNLOAD_TIMEOUT': 2,
        'MONGO_FRESHPROXY_PIPELINE_ENABLED' :False,
        'MONGO_STABLEPROXY_PIPELINE_ENABLED' :False,
    }


    def start_requests(self):
        https_url = 'https://icanhazip.com/'
        proxy = requests.get(url="http://10.221.128.67:5000/proxy/i/https").text
        print(proxy)
        yield scrapy.Request(https_url,callback=self.parse,meta={'proxy':proxy}
           ,dont_filter=True)
           

    #返回proxyItemWrapper，标记代理是否可用
    def parse(self,response): 
        print(response)
        yield {
            "ip":response.css('body p::text').get()
        }
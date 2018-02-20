#coding=utf-8
import scrapy
import types
import sys
#import redis
from bugs.items import DmozItem
from scrapy.loader import ItemLoader
from scrapy.http import Request
from scrapy.loader.processors import MapCompose,Join
import logging
from scrapy.spider import CrawlSpider,Rule
import re
import urlparse
class DmozSpider(CrawlSpider):
    name = "dmoz"
    allowed_domains = ["csdn.net","blog.csdn.net"]
    start_urls = [
        "https://blog.csdn.net"
    ]

    def parse(self, response):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        next_selector=response.xpath("//a/@href")
        for url in next_selector.extract():
            if re.match("http",url):
                if not re.match('http://my.csdn.net*', url) \
                        and not re.match('https://edu.csdn.net*', url) \
                        and not re.match('javascript*', url) \
                        and not re.match('http://ask.csdn.net*', url) \
                        and not re.match('http://www.csdn.net*', url) \
                        and not re.match('http://download.csdn.net*',url) \
                        and not re.match('http://huiyi.csdn.net*', url):
                    yield Request(urlparse.urljoin(response.url,url))

        selector=response.xpath("//a")
        s1=response.xpath('//div/ul/li/a')

        selector = selector+s1
        for s in selector:
            yield self.parse_item(s,response)


    def parse_item(self,selector,response):
        l=ItemLoader(item=DmozItem(),selector=selector)
        l.add_xpath('title','./text()',MapCompose(unicode.strip,unicode.title))
        l.add_xpath('link','./@href',MapCompose(lambda i: urlparse.urljoin(response.url,i)))
        #logging.critical(l.load_item())
        #logging.critical("after parse")
        return l.load_item()




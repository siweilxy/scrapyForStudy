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
        "https://www.csdn.net/"
    ]

    def parse(self, response):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        next_selector=response.xpath("//div/a//@href")
        for url in next_selector.extract():
            res=re.match("http",url)
            #logging.critical(response.url)
            if res:
                yield Request(urlparse.urljoin(response.url,url))

        selector=response.xpath("//div/a")
        for s in selector:
            yield self.parse_item(s,response)


    def parse_item(self,selector,response):
        l=ItemLoader(item=DmozItem(),selector=selector)
        l.add_xpath('title','./text()',MapCompose(unicode.strip,unicode.title))
        l.add_xpath('link','./@href',MapCompose(lambda i: urlparse.urljoin(response.url,i)))
        #logging.critical(l.load_item())
        #logging.critical("after parse")
        return l.load_item()
"""""
    def parse(self, response):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        #print("parse start:")
        #filename = response.url.split("/")[-2]
        items=[]
        divs= response.xpath('//div')
        for p in divs.xpath('.//a'):
            url=p.xpath('@href').extract_first()
            title=p.xpath('text()').extract_first()
            if type(title) is types.NoneType:
                continue
            if type(url) is types.NoneType:
                continue

            title=title.strip()
            url=url.strip()
            if url==u'None':
                #print('+++++++++++++++++++++++++1')
                continue
            if len(url)==0:
                #print('++++++++++2')
                continue
            if title==u"":
                continue
            item=DmozItem()
            item['title']=title
            item['link']=url
            items.append(item)
            #res1=re.match("http",item['link'])
            #res2=re.match("https",item['link'])
            #if res1!=None or res2!=None:
                #yield Request(urlparse.urljoin(response.url,url))
                #yield self.parse_items(item)
        #print 4
            #else:
                #print item['link']+'_______________________________________'
        #print("parse end")
        #yield set(items)
        #return set(items)
        for i in items:
            res1=re.match("http",i['link'])
            res2=re.match("https",i['link'])
            if res1!=None or res2!=None:
                print("add to url",i['link'],"text is ",i['title'])
                yield Request(urlparse.urljoin(response.url,i['link']))
        yield self.parse_items(items)

    def parse_items(self,item):
        print "return"
        return set(item)
        """




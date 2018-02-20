# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import redis
import re
import logging
from scrapy.http import Request
import scrapy

class BugsPipeline(object):

    def __init__(self):
        self.list=set()

    def process_item(self, item, spider):
        if 'title' in item and 'link' in item:
            title=item['title'][0]
            link=item['link'][0]
            #logging.critical(title)
            #logging.critical(link)
            if re.match('http://my.csdn.net*',link) \
                    or re.match('https://edu.csdn.net*',link) \
                    or re.match('javascript*',link)\
                    or re.match('http://ask.csdn.net*',link)\
                    or re.match('http://www.csdn.net*',link):
                logging.critical("link is not needed")
                logging.critical(link)
                return item
            #if re.match('http://blog.csdn.net*',link):
                #logging.critical("blog.csdn.net is needed")
            if title not in self.list:
                self.list.add(title)
                r = redis.Redis(host='192.168.1.16', port=6379, db=0)
                logging.critical(item['title'][0])
                r.set(item['title'][0], item['link'][0])  # 添加
                return item
            #link = r.get(item['title'])
            #result = re.match("http", link)
            # if result==None:
            # logging.critical(link)  # 获取
            # logging.critical(item['title'])
            # logging.critical("+++++++++++++++++++++++++++++++++++++++ process end+++++++++++++++++++++++++++++++++++++++")
        #elif 'title' in item:
            #logging.critical("+++++++++++++++++++++++++++++++++++++++1212")
            #logging.critical("测试")
            #logging.critical(item['title'][0])
        #elif 'link' in item:
            #logging.critical(item['link'])
        #print "process end"


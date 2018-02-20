import time
import os

i=0
while(1):
    print "*********************************************************"
    os.system("scrapy crawl dmoz")
    print "*********************************************************"
    time.sleep(1)
    i=i+1
    print "i is "+str(i)
FROM siwei/ubuntu
MAINTAINER siwei

copy bugs/ bugs/
copy scrapy.cfg /
copy startBug.py /
CMD python startBug.py

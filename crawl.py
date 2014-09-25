import os
from billiard import Process
from twisted.internet import reactor
from scrapy import log, signals
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings
from rlfspider.spiders.fb import FbSpider

os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'rlfspider.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realfie.settings.default')

class CrawlerProcess(Process):
        def __init__(self, rlf_user):
            Process.__init__(self)
            
            crawler = Crawler(get_project_settings())
            crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
            crawler.configure()
            
            self.crawler = crawler
            self.spider = FbSpider(rlf_user)

        def run(self):
            settings = self.crawler.settings
            self.crawler.crawl(self.spider)
            self.crawler.start()
            log.start(logfile=settings['LOG_FILE'], loglevel=settings['LOG_LEVEL'], logstdout=settings['LOG_STDOUT'])
            reactor.run()

def run_spider(fbid):
    crawler = CrawlerProcess(fbid)
    crawler.start()
    crawler.join()

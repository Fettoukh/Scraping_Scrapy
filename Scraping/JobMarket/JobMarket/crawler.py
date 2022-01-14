import scrapy
from scrapy import spiderloader
from scrapy.utils import project
from scrapy.crawler import CrawlerRunner
from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor


@inlineCallbacks
def crawl():
    settings = project.get_project_settings()
    spider_loader = spiderloader.SpiderLoader.from_settings(settings)
    spiders = spider_loader.list()
    classes = [spider_loader.load(name) for name in spiders]
    runner = CrawlerRunner(settings)
    for my_spider in classes:
        print(my_spider)
        yield runner.crawl(my_spider)
    reactor.stop()

crawl()
reactor.run()
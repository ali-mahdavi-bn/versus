from backbone.crawler.crawl import Crawler
from product.domain.commands import CategoryVersus
from product.spider.category_versus_spider import CategoryVersusSpider


def category_versus_handler(command: CategoryVersus, crw: Crawler):
    crw.start_worker(CategoryVersusSpider)


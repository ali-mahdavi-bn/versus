
from backbone.crawler.crawl import Crawler
from product.domain.commands import ProductVersus
from product.spider.product_versus_spider import ProductVersusSpider


def product_versus_handler(command: ProductVersus, crw: Crawler):
    crw.start_worker(ProductVersusSpider)


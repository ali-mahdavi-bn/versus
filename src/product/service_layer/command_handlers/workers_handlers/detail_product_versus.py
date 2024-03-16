from backbone.crawler.crawl import Crawler
from product.domain.commands import DetailProductVersus
from product.spider.detail_product_versus_spider import DetailProductVersusSpider


def detail_product_versus_handler(command: DetailProductVersus):
    crw = Crawler()
    crw.start_worker(DetailProductVersusSpider)

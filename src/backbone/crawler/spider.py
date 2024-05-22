from typing import Iterator

from backbone.crawler.helper.adapter.abstract_spider import AbstractSpider
from backbone.crawler.helper.helpers.requests import RequestArgs


class Spider(AbstractSpider):
    def start_requests(self, **kwargs) -> Iterator[RequestArgs]:
        raise NotImplementedError


    def from_crawler(cls, crawler=None) -> Iterator[start_requests]:
        try:
            yield from cls.start_requests()
        except Exception as e:
            print(e)
            yield []

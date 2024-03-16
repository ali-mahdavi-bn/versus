from abc import ABC, abstractmethod
from typing import Any, Self


class AbstractSpider(ABC):
    @abstractmethod
    def from_crawler(self, crawler=None) -> Self: pass

    @abstractmethod
    def start_requests(self, crawler=None) -> Self: pass


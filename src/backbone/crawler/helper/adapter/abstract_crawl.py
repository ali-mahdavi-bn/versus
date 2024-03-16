from abc import ABC, abstractmethod


class AbstractCrawl(ABC):

    @abstractmethod
    def _lifespan(self, lifespan):pass

    @abstractmethod
    def start(self,spider): pass


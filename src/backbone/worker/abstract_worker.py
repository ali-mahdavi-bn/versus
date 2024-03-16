from abc import ABC, abstractmethod


class AbstractWorker(ABC):

    @abstractmethod
    def _lifespan(self, lifespan):pass

    @abstractmethod
    def start(self,spider): pass


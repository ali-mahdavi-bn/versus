from abc import ABC, abstractmethod

from backbone.service_layer.general_types import Query, Params


class Execute(ABC):

    @abstractmethod
    def fetch(self):
        pass

    @abstractmethod
    def fetchall(self):
        pass


class Filter(ABC):

    @abstractmethod
    def filter(self):
        pass

    @abstractmethod
    def first(self):
        pass

    @abstractmethod
    def all(self):
        pass


class AbstractOrm(ABC):
    def execute(self, query: Query, params: Params = None) -> Execute:
        self._execute(query, params)
        return self

    @abstractmethod
    def _execute(self, query: Query, params: Params = None):
        raise NotImplementedError

    def all(self):
        return self._all()

    @abstractmethod
    def _all(self):
        raise NotImplementedError

    def filter(self, *args, **kwargs) -> Filter:
        self._filter(*args, **kwargs)
        return self

    @abstractmethod
    def _filter(self, *args, **kwargs):
        raise NotImplementedError

    def first(self):
        return self._first()

    @abstractmethod
    def _first(self):
        raise NotImplementedError

    def fetch(self):
        return self._fetch()

    @abstractmethod
    def _fetch(self):
        raise NotImplementedError

    def fetchall(self):
        return self._fetchall()

    @abstractmethod
    def _fetchall(self):
        raise NotImplementedError

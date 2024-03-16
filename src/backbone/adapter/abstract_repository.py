from abc import ABC, abstractmethod
from typing import Set, Any


class AbstractRepository(ABC):
    def __init__(self):
        self.seen = set()  # type: Set[Any]

    def add(self, model: any):
        self._add(model)
        self.seen.add(model)

    @abstractmethod
    def _add(self, model):
        raise NotImplementedError

    @property
    def soft_delete_field(self):
        return "deleted_at"

    def delete(self, model: any, soft_delete=True):
        self._delete(model, soft_delete)

    @abstractmethod
    def _delete(self, model, soft_delete: bool):
        raise NotImplementedError

    def find_by_id(self, identifier):
        data = self._find_by_id(identifier)
        if data:
            data.events = []
            self.seen.add(data)
        return data

    @abstractmethod
    def _find_by_id(self, identifier):
        raise NotImplementedError

    def find_by_uuid(self, identifier):
        data = self._find_by_uuid(identifier)
        if data:
            data.events = []
            self.seen.add(data)
        return data

    @abstractmethod
    def _find_by_uuid(self, identifier):
        raise NotImplementedError

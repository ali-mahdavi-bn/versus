from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List

from backbone.adapter.abstract_sqlalchemy_repository import AbstractSqlalchemyRepository


class AbstractUnitOfWork(ABC):

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # close transaction in all condition (if error occurred or not)
        self.rollback()

    def commit(self):
        self._commit()

    def repositories(self) -> List[AbstractSqlalchemyRepository]:
        pass

    def collect_new_events(self):
        for repository in self.repositories():
            for model in repository.seen:
                if hasattr(model, "events"):
                    while model.events:
                        yield model.events.pop(0)

    @abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError

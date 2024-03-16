from abc import ABC, abstractmethod
from typing import Optional, List, Any, Dict, Union

from backbone.adapter.abstract_sqlalchemy_repository import AbstractSqlalchemyRepository
# from unit_of_work import UnitOfWork


class AbstractApiResource(ABC):
    def __init__(self, uow=None):
        self.uow: AbstractSqlalchemyRepository = uow

    @abstractmethod
    def make(self, model: Any, **kwargs) -> Dict:
        raise NotImplementedError

    def optional(self, model: Any, **kwargs) -> Union[None, Dict]:
        return self.make(model, **kwargs) if model else None

    @classmethod
    def json(cls, data: Optional[Dict] = None, **kwargs) -> Dict:
        if data is None:
            data = {}

        return {**data,
                **kwargs
                }

    def collection(self, models: List[Any]) -> List[Dict]:
        return [self.make(model) for model in models]

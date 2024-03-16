from abc import ABC

from backbone.adapter.abstract_repository import AbstractRepository
from backbone.adapter.abstract_sqlalchemy_repository import AbstractSqlalchemyRepository
from product.domain.entities import ProductTranslate


class AbstractTranslateProductRepository(AbstractRepository, ABC):
    pass


class SqlalchemyTranslateProductRepository(AbstractTranslateProductRepository, AbstractSqlalchemyRepository):
    @property
    def model(self):
        return ProductTranslate

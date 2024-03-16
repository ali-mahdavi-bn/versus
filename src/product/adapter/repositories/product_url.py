from abc import ABC

from backbone.adapter.abstract_repository import AbstractRepository
from backbone.adapter.abstract_sqlalchemy_repository import AbstractSqlalchemyRepository
from product.domain.entities import Category, ProductUrl


class AbstractProductUrlRepository(AbstractRepository, ABC):
    pass


class SqlalchemyProductUrlRepository(AbstractProductUrlRepository, AbstractSqlalchemyRepository):
    @property
    def model(self):
        return ProductUrl

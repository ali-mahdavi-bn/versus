from abc import ABC

from backbone.adapter.abstract_repository import AbstractRepository
from backbone.adapter.abstract_sqlalchemy_repository import AbstractSqlalchemyRepository
from product.domain.entities import Product, Language


class AbstractLanguageRepository(AbstractRepository, ABC):
    pass


class SqlalchemyLanguageRepository(AbstractLanguageRepository, AbstractSqlalchemyRepository):
    @property
    def model(self):
        return Language


from abc import ABC

from backbone.adapter.abstract_repository import AbstractRepository
from backbone.adapter.abstract_sqlalchemy_repository import AbstractSqlalchemyRepository
from product.domain.entities.attribute_translate import AttributeTranslate


class AbstractTranslateCategoryRepository(AbstractRepository, ABC):
    pass


class SqlalchemyTranslateCategoryRepository(AbstractTranslateCategoryRepository, AbstractSqlalchemyRepository):
    @property
    def model(self):
        return AttributeTranslate

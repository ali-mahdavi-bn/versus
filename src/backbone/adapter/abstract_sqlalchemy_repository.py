import datetime
from abc import abstractmethod
from typing import TypeVar, Generic
from uuid import UUID

from sqlalchemy.orm import Query

from backbone.adapter.abstract_entity import BaseEntity
from backbone.adapter.abstract_repository import AbstractRepository
from backbone.adapter.abstract_sqlalchemy_orm import SqlAlchemyOrm

ENTITY = TypeVar("ENTITY", bound=BaseEntity)


class AbstractSqlalchemyRepository(AbstractRepository, Generic[ENTITY]):
    def __init__(self, session):
        self.orm = SqlAlchemyOrm(model=self.model, session=session)
        self.session = session

        super().__init__()

    def _add(self, model: ENTITY):
        self.session.add(model)

    def _delete(self, model: ENTITY, soft_delete=True):
        if not soft_delete:
            self.session.delete(model)
            return

        if soft_delete and hasattr(model, self.soft_delete_field):
            setattr(model, self.soft_delete_field, datetime.datetime.now())
        else:
            raise Exception(f"{self.model} hasn't attribute {self.soft_delete_field}")

    @property
    @abstractmethod
    def model(self) -> ENTITY:
        raise NotImplementedError

    # @property
    # def query(self, ) -> Query:
    #     return self.session.query(self.model)

    def _find_by_id(self, identifier) -> ENTITY:
        data = self.orm.query.filter(self.model.id == identifier).first()
        return data

    def _find_by_uuid(self, identifier: UUID) -> ENTITY:
        if not hasattr(self.model, "uuid"):
            raise Exception(f"{type(self.model)} hasn't uuid attr")
        data = self.orm.query.filter(self.model.uuid == identifier.__str__()).first()
        return data

    def _find_by_uuid_and_org(self, identifier: UUID, organization_id: UUID) -> ENTITY:
        if not hasattr(self.model, "uuid") or not hasattr(self.model, "organization_id"):
            raise Exception(f"{type(self.model)} hasn't uuid attr or organization_id attr")
        data = self.orm.query.filter(self.model.uuid == identifier.__str__(),
                                 self.model.organization_id == organization_id.__str__()).first()
        return data

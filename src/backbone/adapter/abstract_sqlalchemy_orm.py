from sqlalchemy import text
from sqlalchemy.orm import Session

from backbone.adapter.abstract_orm import AbstractOrm


class SqlAlchemyOrm(AbstractOrm):
    filters = None

    def __init__(self, session, model):
        self._query_sql = None
        self.model: Session = model
        self._session: Session = session
        self._query_obj = None

    def _fetch(self):
        if not self._query_obj:
            raise ValueError("not execute query")
        return self._query_obj.fetchone()

    def _fetchall(self):
        if not self._query_obj:
            raise ValueError("not execute query")
        return self._query_obj.fetchall()

    def _execute(self, query: str, params=None):
        if not query:
            raise ValueError("i need query")
        self._query_obj = self._session.execute(text(query), params)
        return self

    def _all(self):
        return self.query.all()

    @property
    def query(self):
        return self._session.query(self.model)

    def _filter(self, *args, **kwargs):

        for arg in args:
            if self.filters:
                self.filters = self.filters.filter(arg)
            self.filters = self.query.filter(arg)
        return self

    def _first(self):
        if not self.filters:
            raise ValueError("i need filter")
        return self.filters.first()

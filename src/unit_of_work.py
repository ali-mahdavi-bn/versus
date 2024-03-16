from __future__ import annotations

from backbone.infrastructure.databases.postgres_connection import DEFAULT_SESSION_FACTORY
from backbone.service_layer.abstract_unit_of_work import AbstractUnitOfWork
from product.adapter import repositories as product_repo


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, postgres_session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = postgres_session_factory

    def __enter__(self) -> 'UnitOfWork':

        self.session = self.session_factory(expire_on_commit=False)  # type: Session
        self.product_url = product_repo.SqlalchemyProductUrlRepository(self.session)
        self.product = product_repo.SqlalchemyProductRepository(self.session)
        self.language = product_repo.SqlalchemyLanguageRepository(self.session)
        self.translate_category = product_repo.SqlalchemyTranslateCategoryRepository(self.session)
        self.translate_product = product_repo.SqlalchemyTranslateProductRepository(self.session)
        self.category = product_repo.SqlalchemyCategoryRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.expunge_all()
        # self.session.close()

    def repositories(self):
        repos = []
        try:
            pass
        except:
            pass
        return repos

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.expunge_all()
        # self.session.rollback()

from uuid import UUID

from backbone.service_layer.general_types import Command, Dao


class CategoryVersus(Command): pass


class ProductVersus(Command): pass


class SearchProducts(Command):
    filters: dict
    category_id: UUID
    language: int
    limit: int
    page: int


class DetailProductVersus(Command): pass


class GetProduct(Dao):
    product_slug: str
    language: int

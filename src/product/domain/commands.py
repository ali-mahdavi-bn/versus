from typing import Optional
from uuid import UUID

from backbone.service_layer.general_types import Command


class CategoryVersus(Command): pass


class ProductVersus(Command): pass


class SearchProducts(Command):
    filters: dict
    category_id: UUID
    language: int
    limit: int
    page: int


class DetailProductVersus(Command): pass


class GetProduct(Command):
    product_id: str
    language: int

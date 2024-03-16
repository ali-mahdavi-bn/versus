from uuid import UUID

from backbone.adapter.abstract_entity import BaseEntity
from backbone.service_layer.general_types import ID, ForeignKeyUuid


class ProductUrl(BaseEntity):
    id: ID
    url: str
    category_id: ForeignKeyUuid

    @classmethod
    def create(cls, url=None, category_id=None, ts=None):
        product = ProductUrl()
        product.url = url
        product.ts = ts
        product.category_id = category_id
        return product

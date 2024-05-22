from datetime import datetime
from uuid import UUID

from backbone.adapter.abstract_entity import BaseEntity
from backbone.service_layer.general_types import ID, Name, CreatedAt, UpdatedAt, DeletedAt, ForeignKeyUuid


class ProductTranslate(BaseEntity):
    id: ID
    uuid: UUID
    product_id: ForeignKeyUuid
    language: int
    name: Name
    description: str
    created_at: CreatedAt
    updated_at: UpdatedAt
    deleted_at: DeletedAt

    @classmethod
    def create(cls, name=None, description=None, language=None, uuid=None, product_id=None):
        translate_product = ProductTranslate()
        translate_product.uuid = uuid
        translate_product.product_id = product_id
        translate_product.name = name
        translate_product.language = language
        translate_product.description = description

        return translate_product

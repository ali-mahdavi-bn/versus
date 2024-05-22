from datetime import datetime
from uuid import UUID

from backbone.adapter.abstract_entity import BaseEntity
from backbone.service_layer.general_types import ID, CreatedAt, UpdatedAt, DeletedAt, ForeignKeyUuid


class ProductValue(BaseEntity):
    id: ID
    category_attribute_id: ForeignKeyUuid
    product_id: str
    value: str
    value_int: int
    unit: str
    type: str
    created_at: CreatedAt
    updated_at: UpdatedAt
    deleted_at: DeletedAt

    @classmethod
    def create(cls, value=None, value_int=None, unit=None, product_id=None, category_attribute_id=None):
        product_value = ProductValue()
        product_value.value = value
        product_value.value_int = value_int
        product_value.unit = unit
        product_value.product_id = product_id
        product_value.category_attribute_id = category_attribute_id

        return product_value

from datetime import datetime
from uuid import UUID

from backbone.adapter.abstract_entity import BaseEntity
from backbone.service_layer.general_types import ID, IsActive, CreatedAt, UpdatedAt, DeletedAt, ForeignKeyUuid


class Product(BaseEntity):
    id: ID
    uuid: UUID
    image_src: str
    slug: str
    category_id: ForeignKeyUuid
    is_active: IsActive
    created_at: CreatedAt
    updated_at: UpdatedAt
    deleted_at: DeletedAt

    @classmethod
    def create(cls, image_src=None, is_active=True, uuid=None, category_id=None, slug=None):
        product = Product()
        product.uuid = uuid
        product.image_src = image_src
        product.slug = slug
        product.category_id = category_id
        product.is_active = is_active
        return product

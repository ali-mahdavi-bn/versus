from uuid import UUID

from backbone.adapter.abstract_entity import BaseEntity
from backbone.service_layer.general_types import ID, CreatedAt, UpdatedAt, DeletedAt, ForeignKeyUuid, Slug


class Attributes(BaseEntity):
    id: ID
    uuid: UUID
    category_id: ForeignKeyUuid
    group_attribute_id: ForeignKeyUuid
    slug: Slug
    is_searchable: bool
    is_show: bool
    smaller_better: bool
    created_at: CreatedAt
    updated_at: UpdatedAt
    deleted_at: DeletedAt

    @classmethod
    def create(cls, category_id=None, type=None, slug=None,group_attribute_id=None, translate_category_id=None,
               smaller_better=None, uuid=None):
        category_attribute = Attributes()
        category_attribute.uuid = uuid
        category_attribute.type = type
        category_attribute.slug = slug
        category_attribute.category_id = category_id
        category_attribute.smaller_better = smaller_better if smaller_better else False
        category_attribute.group_attribute_id = group_attribute_id
        category_attribute.translate_category_id = translate_category_id

        return category_attribute

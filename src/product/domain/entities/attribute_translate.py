from datetime import datetime
from uuid import UUID, uuid4

from backbone.adapter.abstract_entity import BaseEntity
from backbone.service_layer.general_types import ID, Name, CreatedAt, UpdatedAt, DeletedAt, ForeignKeyUuid


class AttributeTranslate(BaseEntity):
    id: ID
    uuid: UUID
    category_attribute_id: ForeignKeyUuid
    language: int
    show_name: str
    name: Name
    description: str
    created_at: CreatedAt
    updated_at: UpdatedAt
    deleted_at: DeletedAt

    @classmethod
    def create(cls, show_name=None, name=None, description=None, language=None, uuid=None, category_attribute_id=None):
        translate_category = AttributeTranslate()
        translate_category.uuid = uuid if uuid else uuid4()
        translate_category.show_name = show_name
        translate_category.name = name
        translate_category.category_attribute_id = category_attribute_id
        translate_category.description = description
        translate_category.language = language

        return translate_category
